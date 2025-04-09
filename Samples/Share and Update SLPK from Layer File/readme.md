# Share and Update SLPK from Layer File

Automate sharing and updating a SLPK from a layer file.


## Use Case
A transportation digital twin in Zurich needs to be updated to reflect that a decommissioned railway track was demolished and removed. Keeping the engineering data current in the digital twin benefits many stakeholders. In Civil 3D, an engineer modifies the railway track engineering data, modeled as corridor objects. The sample script can be used to create functionality that updates the engineering data in the digital twin, so that web scenes that references the scene layer shows the updated railway track segment in the digital twin. 


## Requirements
- Please have a .lyrx file prepared before using the sample script. See [how to save a .lyrx file](https://pro.arcgis.com/en/pro-app/latest/help/sharing/overview/save-a-layer-file.htm#:~:text=Select%20the%20layer%20or%20table,file%20in%20the%20Contents%20pane.&text=On%20the%20Save%20Layer(s,Click%20Save. ) for more information.

## How to use the sample.
Download the ArcPy script (link it) in this folder and adjust it as needed. Optionally, download the sample [service track layer file](Service_Track.lyrx) and [Zurich trainyard drawing](Zurich_Trainyard.dwg) in this folder to use with the script.
