# Update a Scene Layer from Civil 3D Using a Layer File

Automate updating a scene layer from a layer file (.lyrx) to ArcGIS Online.

![image](https://github.com/user-attachments/assets/cf92ca3d-3633-45c7-abc3-a8e71a1d2b7b)

## Use Case
A transportation digital twin in Zurich needs to be updated to reflect that a decommissioned railway track was demolished and removed. Keeping the engineering data current in the digital twin benefits many stakeholders. Using ArcPy, engineers working in Civil 3D can modify the corridor objects. This sample script updates the digital twins and web scenes that reference the scene layer have the latest information.

## Requirements
- Have a .lyrx file prepared before using the sample script. See [how to save a .lyrx file](https://pro.arcgis.com/en/pro-app/latest/help/sharing/overview/save-a-layer-file.htm#:~:text=Select%20the%20layer%20or%20table,file%20in%20the%20Contents%20pane.&text=On%20the%20Save%20Layer(s,Click%20Save. ) for more information.

## How to use the sample.
Download the [ArcPy script](SceneLayer.py) in this folder and adjust it as needed. Optionally, download the sample [service track layer file](Service_Track.lyrx) and [Zurich trainyard drawing](Zurich_Trainyard.dwg) in this folder to use with the script.
