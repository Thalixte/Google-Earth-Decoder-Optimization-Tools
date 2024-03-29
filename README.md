# Google-Earth-Decoder-Optimization-Tools
Python blender addon designed to be used with Google Earth Decoder Tool sceneries

<p class="md-badges">
<a href="https://hits.seeyoufarm.com" target="_blank"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FThalixte%2FGoogle-Earth-Decoder-Optimization-Tools&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true" class="md-badge"/></a>
<img src="https://img.shields.io/github/license/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/v/release/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/stars/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/forks/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/issues/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">


</p>

**1) Presentation:**

This blender addon is designed to provide tools to help optimizing city sceneries, retrieved via the Google Earth Decoder Tool, made by u/Jonahex111.

This addon is coded in Python, and sources are available here: https://github.com/Thalixte/Google-Earth-Decoder-Optimization-Tools.

**2) Prerequisites:**

* Blender 2.83 or superior

* Optional: to reduce the number of texture files, you can get the Lily texture Packer. Download version 1.1.x if you use Blender 2.83. If you use Blender 3.x, you can use the last version. Reducing the number of texture files reduce the loading time of the scenery, and can reduce stuttering related to texture streaming inside the sim

* Optional: once your package has been successfully built, you can further reduce its size by using the "Optimize the bulilt package by compressing the texture files" entry of the addon menu. To do so, you have to download the Compressonator tool from GPUOpen.

**3) Installation:**

Download the Google-Earth-Decoder-Optimization-Tools.zip archive. In Blender, open the preferences window: Edit > Preferences..., then select the Add-ons tab. Click on the Install... button, then browse to the archive you have just downloaded. Once installed, enable the addon.
If everything worked correctly, you should see a new menu in Blender, called "Google Earth Decoder Optimization Tools".

**4) Usage:**

Open the "Google Earth Decoder Optimization Tools" menu in Blender.

Choose an action from the menu entries:

* **Initialize a new Msfs scenery project:**
This script creates the MSFS structure of a scenery project, if it does not already exist.
Once created, you can copy the result of the Google Earth decoder Output folder into the PackageSources folder of the newly created project. 
You can also create the structure, then in the Google Earth Decoder tool, point the Output folder to the PackageSources folder of the project.
The structure is the same as the one provided in the SimpleScenery project of the MSFS SDK samples.


* **Optimize an existing Msfs scenery project:**
This script optimizes an existing Google Earth Decoder scenery project (textures, Lods, CTD fix).
If you installed and enabled the Lily Texture Packer Blender addon, and you ticked the "Bake textures enabled" checkbox in the tool menu (section PROJECT), the textures of the project are merged per tile lods, which significantly reduce the number of the project files.
It fixes the bounding box of each tile in order for them to fit the MSFS lod management system.
This script also adds Asobo extension tags in order to manage collisions, road traffic, and correct lightning.
 

* **Clean the unused files of the msfs project:**
This script cleans the unused files of the MSFS scenery project.
Once you removed some tiles of a project, use this script to clean the gltf, bin and texture files associated to those tiles.
Merge an existing MSFS scenery project into another one:


* **Merge the tiles of a MSFS scenery project into another MSFS scenery project:**
This script merges the tiles of a MSFS scenery project into another MSFS scenery project.
In the MERGE section, select the project that you want to merge into the project indicated in the PROJECT section.

**Update the position of the MSFS scenery tiles:**
This script calculates the position of the MSFS scenery tiles.
If you are not satisfied with the resulting positions, you can setup a latitude correction and/or a longitude correction in the TILE section.


* **Update LOD min size values for each tile of the project:**
This script updates the LOD min size values for each tile of the project.
In the LODS section, you can setup each minsize value of each LOD level.
According to the MSFS SDK documentation, the selection process is as follows:
starting from LoD 0, going down, the first LoD with a minSize smaller than the model's current size on screen will be selected for display.
The selection will also take into account forced and disabled LoDs as configured by the model options.


* **Fix lightning issues on tiles at dawn or dusk:**
This script fixes the lightning issues on tiles at dawn or dusk.
To do so, it adds a specific Asobo extension tag ("ASOBO_material_fake_terrain") in the gltf files corresponding to the tiles Lod levels.


* **Optimize the built package by compressing the texture files:**
This script optimizes the built package of a MSFS scenery project by compressing the DDS texture files.
For the script to process correctly, the package must have been successfully built prior to executing the script.


* **Add a collider for each tile of the project:**
This is an extra optimization of the scenery, wich is totally optional. When the scenery is optimized using the "Optimize an existing Msfs scenery project" script, the collision detection tags and the road tags are included in all the lods, which can produce CPU overload (even if my tests indicate that this is not really significant, in my config with a relatively old Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz). This script removes the collision and road tags for all the LODs, and creates a specific transparent collider that embeds those tags for each tile of the project. Each collider object is created from the less detailed lod tile to decrease the CPU overload.


* **Remove the colliders for each tile of the project:**
This script removes all the colliders objects that have been created with the "Add a collider for each tile of the project" script. It also reverts back the road and collision tags for all the lods.

If you want to donate, you will always be welcome to help me continue with more projects and update the existing ones https://paypal.me/Thalixte.
