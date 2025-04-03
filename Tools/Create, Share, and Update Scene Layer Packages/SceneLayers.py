import arcpy
from arcgis.gis import GIS
import time
import os

# Sign into ArcGIS Online for Arcpy & ArcGIS Python API
print("Signing in to ArcGIS Online")
portal = 'https://arcgis.com'
username = 'username'
password = 'password'
arcpy.SignInToPortal(portal, username, password)
gis = GIS(portal, username, password)

# Setup to create scene layer package from existing layer definition
lyrx_file = r'C:\projects\ZurichRailLines\Service_Track.lyrx'
slpk_path = r'C:\projects\ZurichRailLines\temp'
slpk_sr = arcpy.SpatialReference(4326)
destinationSceneLayerID = "z3a4276hn7b224d1el987a66b7e55"

# Create scene layer package with new content
print("Creating scene layer package")
baseFileName = "Service_Track" + time.strftime("%Y%m%d_%H%M%S")
slpk_file = os.path.join(slpk_path, baseFileName + '.slpk')
arcpy.management.Create3DObjectSceneLayerPackage(lyrx_file, slpk_file, slpk_sr, None, 'DESKTOP')

# Share the new scene layer and get the new layer ID
print("Sharing scene layer to ArcGIS Online")
SharedLayer = arcpy.management.SharePackage(slpk_file, "", "", "", "", "", "", None, "EVERYBODY", True, None)
search_result = gis.content.search(baseFileName, item_type="Scene Layer")
newSceneLayerID = search_result[0].id 
print(newSceneLayerID)

# Replace existing scene layer with the updated version
print("Updating destination web scene layer")
archiveLayerName = baseFileName + '_archive'
arcpy.server.ReplaceWebLayer(destinationSceneLayerID, archiveLayerName, newSceneLayerID, "Keep", "True")
print("Scene layer updated")