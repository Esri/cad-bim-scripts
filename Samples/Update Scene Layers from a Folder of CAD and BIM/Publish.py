"""
   Copyright 2025 Esri

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.​

This sample replaces existing web scene layers for a collection of updated CAD and BIM files.
"""

import os
import time
import json
import arcpy
from arcgis.gis import GIS

# Set credentials and workspace
portal_url = "https://arcgis.com"
username = ""
password = ""
workspace = r"C:\...\design"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

def get_basename(file_path):
    """Returns a sanitized base name accepted by ArcGIS Pro"""
    return ''.join(e for e in os.path.splitext(os.path.basename(file_path))[0] if e.isalnum())

def get_spatial_reference(model):
    """Returns spatial reference from a universal PRJ file (case-insensitive), otherwise defaults to WGS84."""
    universal_prj = next((os.path.join(workspace, f) for f in os.listdir(workspace) if f.lower() == "esri_cad.prj"),
                         None)
    model_prj = os.path.join(workspace, os.path.splitext(os.path.basename(model))[0] + ".prj")
    sr = (arcpy.SpatialReference(model_prj) if os.path.isfile(model_prj)
          else arcpy.SpatialReference(universal_prj) if universal_prj and os.path.isfile(universal_prj)
          else arcpy.SpatialReference(4326))  # Default to WGS84
    print(f"{model} spatial reference: {sr.name}")
    return sr

def process_bim_files(bim_files):
    """Processes BIM files and creates Building Scene Layer Packages (SLPKs)."""
    slpks = []
    for bim_file in bim_files:
        dataset_name = get_basename(bim_file)
        slpk_file = dataset_name + ".slpk"
        arcpy.management.MakeBuildingLayer(bim_file, dataset_name)
        arcpy.management.CreateBuildingSceneLayerPackage(dataset_name, slpk_file)
        slpks.append(slpk_file)
    return slpks
    
def process_cad_files(cad_files):
    """Processes CAD files and creates 3D Object Scene Layer Packages (SLPKs) from its MultiPatch feature class"""
    slpks = []
    for cad_file in cad_files:
        dataset_name = get_basename(cad_file)
        lyrx_file = dataset_name + ".lyrx"
        slpk_file = dataset_name + ".slpk"
        spatial_ref = get_spatial_reference(cad_file)
        multipatch_fc = os.path.join(cad_file, 'MultiPatch')
        arcpy.management.MakeFeatureLayer(multipatch_fc, dataset_name)
        arcpy.management.SaveToLayerFile(dataset_name, lyrx_file, "RELATIVE")
        arcpy.management.Create3DObjectSceneLayerPackage(lyrx_file, slpk_file, spatial_ref, None, "DESKTOP")
        slpks.append(slpk_file)
    return slpks
def publish(slpk):
    """Publishes an SLPK file and a web scene layer"""
    res = arcpy.management.SharePackage(slpk, username, password, public="EVERYBODY", publish_web_layer=True)
    if res[0]:  # If successful
        print(f"Published {slpk}.\nPortal ID: {res[1]}\nJSON: {res[2]}")
        return json.loads(res[1])["publishResult"]["serviceItemId"]

def replace(slpk, target_layer, update_layer):
    """Replace a (target) scene layer with the new layer we published"""
    archive_layer_name = slpk.split(".")[0] + time.strftime("%Y%m%d_%H%M%S")
    return arcpy.server.ReplaceWebLayer(target_layer,archive_layer_name, update_layer, "REPLACE", True)

# Append BIM and CAD files to a list separably
bim_files = [f for f in os.listdir(workspace) if f.endswith((".rvt", ".ifc"))]
cad_files = [f for f in os.listdir(workspace) if f.endswith((".dwg", ".dgn"))]

# Generate SLPKs for CAD and BIM files
slpks = process_cad_files(cad_files) + process_bim_files(bim_files)

# Publish and replace web scene layers
gis = GIS('home')
arcpy.SignInToPortal(portal_url, username, password)
target_layers = [''] * len(slpks)
target_layers[1] = "dae9fe1383b440df9492501e9296ab55"
target_layers[2] =  "11d58e0ab96a4d66b0386977d3e52be3"
for i, (slpk, target_layer) in enumerate(zip(slpks, target_layers), start=1):
    print(f"Uploading {i}/{len(slpks)}: {slpk}")
    service_item_id = publish(slpk)
    if target_layer:
        updated_layer = replace(slpk, target_layer, service_item_id)
        print(f"Updated web layer URL: {updated_layer}")
