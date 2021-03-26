# Google-Earth-Decoder-optimisation-tools
Python blender scripts designed to be used with Google Earth Decoder Tool sceneries
**
1) Presentation:**  
The archive contains four python scripts:  

*   scenery_optimisation.py: optimize Google Earth Decoder scenery (textures, Lods, CTD fix)
*   fix_tiles_altitudes.py: fix wrong tiles altitudes that can occure when moving tiles on the x-y axis
*   update_objects_LODs.py: update the LOD levels for the tiles of a scenery based on an array of minsizes
*   merge_sceneries: merge all the files from a source Google Earth Decoder scenery to a destination Google Earth Decoder scenery

The scripts are intended to be used with a Google Earth Decoder min LOD of 17\. I did not test them with another Google Earth Decoder minLod.  

**
2) Prerequisites:**  

*   Blender 2.83 ([https://download.blender.org/release/Blender2.83/blender-2.83.9-windows64.msi](https://download.blender.org/release/Blender2.83/blender-2.83.9-windows64.msi)). **The blender version is important**
*   Node js ([https://nodejs.org/dist/v14.15.1/node-v14.15.1-x64.msi](https://nodejs.org/dist/v14.15.1/node-v14.15.1-x64.msi))
*   Blender2MSFS Toolkit: [https://www.fsdeveloper.com/forum/resources/blender2msfs-toolkit.256/download](https://www.fsdeveloper.com/forum/resources/blender2msfs-toolkit.256/download)
*   Lily texture Packer: [https://gumroad.com/l/DFExj](https://gumroad.com/l/DFExj)
**
3) scenery_optimisation script**:  

3.1) Presentation:  
This script applies the CTD issues fix (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery](../../blog/creators-guide-fix-ctd-issues-on-your-scenery)).  
It bakes the tiles texture files in order to reduce the number of the files in the final package, and reduce the scenery loading time.  
It fixes an issue with the Google Earth Decoder tool, that breaks the LOD management system.  
Look at this picture: [https://flic.kr/p/2k3YCrd](https://flic.kr/p/2k3YCrd)  
This picture shows a wireframe representation of a big scenery created from the Google Earth Decoder tool. You can see that the scenery tiles are dark gray, which means there are a lot of vertices on each tile, because all the tiles are on the max level of detail (which is 19 here). The result is that this scene, from this point of view, displays more than 80M of vertices, which bottlenecks the GPU (and the CPU).  
Normally, we should have this: [https://flic.kr/p/2kayM52](https://flic.kr/p/2kayM52). In this case, we can see that the tiles have the correct LOD levels, and it leads to a reduced number of vertices (20M in this case, but it can be changed according to the LOD levels that are set in the optimisation script (see chap. 3.3 - Configuration)).  
The problem here is that the Google Earth Decoder gives all the tiles the same origin, and changes the bounding box to go from this origin point to the last mesh vertice point.  
Another way to see this problem, is to use the new MSFS SDK Debug LOD feature, that displays the current lod level of each tiles, and the size of the bounding sphere: [https://flic.kr/p/2kautrR](https://flic.kr/p/2kautrR)  
The more the green or blue is the color, the more detailed is the tile. The more the yellow or red is the color, the less detailed is the tile.  
Here, we can see that the more detailed tiles are the one that are far from the camera, which is the exact opposite result than the one we want to obtain to optimize our scenery framerate.  
Now, if each tile has its own origin point, and has a bounding box corresponding to the real tile size, we obtain those results: [https://flic.kr/p/2kayiyp](https://flic.kr/p/2kayiyp) and [https://flic.kr/p/2kayiAo](https://flic.kr/p/2kayiAo), which are far better from a LOD point of view, and better preserve the framerate.  
This is the fix that the script applies to the tiles: it gives each tile its own origin point, and resizes the bounding boxes according to the real tile size.  
The script also changes the LOD levels to better suit the LOD management system, and allows (if configured) to convert texture files into jpg format, in order to reduce the texture file size (but with a possible loss in the texture quality).  
The script also applies ASOBO extension tags to the gltf files, in order to enable the road management and the collisions. It also fixes texture flickering issues.  
The script automatically removes the orphaned scenery object xml files (scenery object xml files that do not have associated gltf and/or bin files)  

3.2) Installation:  
Just put the scenery_optimisation.py script, and the retrievepos.js script in a folder of your choice.  

3.3) Configuration:  
Change the following settings, according to your project:  

*   **bake_textures_enabled:** tells the script to optimize the textures by baking all the textures corresponding to the min Lod levels of the tiles (default is True). For instance, if you have a gltf file for a tile that is named 30604141705340627_LOD00.gltf, all the texture files corresponding to this tile and this LOD level (all the texture files that start with 30604141705340627_LOD00) will be baked into one single texture
*   **projects_folder:** the parent folder that contains your sceneries
*   **project_name:** the name of your project
*   **node_js_folder:** the folder that contains the node js script that retrieves the Google Earth coords
*   **fspackagetool_folder:** the folder that contains the fspackagetool exe that builds the MSFS packages
*   **target_lods**: an array representing the minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
*   **project_file_name**: the name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
*   **scene_file_name:** the name of the xml file that embeds the tile descriptions (by default, objects.xml)
*   **package_definitions_file_name**: the name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
*   **author_name:** the name of the author of the scenery
*   **build_package_enabled:** enable the package compilation when the script has finished (default is True)
*   **output_texture_format:** format of the final texture files (values are PNG_FORMAT, JPG_FORMAT, default is PNG_FORMAT)
*   **JPG_COMPRESSION_RATIO:** if you choose the jpg format for the output texture files, indicates the compression ratio

3.4) Usage:  
Open Blender **in administrator mode**.  
Go in the Scripting view, then click on the Open icon, and choose the scenery_optimisation python script.  
When the configuration is done, open the Blender system console Window (Window => Toggle System Console). Then, run the script.  

3.5) Process:  

*   rename the modelLib folder, in order to fix CTD issues (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery](../../blog/creators-guide-fix-ctd-issues-on-your-scenery)/)
*   if no other backup exists, backup the scenery modelLib files into a backup folder, inside the project folder
*   if necessary, install the node Js xhr2 module (npm install xhr2)
*   install the PIP and Pillow libraries to allow texture format conversion
*   if png texture files output format is selected, convert all remaining jpg texture files to PNG, then remove jpg files
*   if jpg texture files output format is selected, convert all remaining png texture files to JPG, then remove png files, and compress all jpg texture files
*   retrieve objects positions from Google earth, via the Google Earth API, and put the results in .pos files corresponding to the scenery tiles
*   update the tiles position, using those .pos files
*   place all tiles objects into corresponding sub folders, in order to group the objects corresponding to the same tile
*   update the LODs of the scenery tiles, according to the target_lods defined in the configuration settings
*   optimize the tiles, by baking the textures corresponding to LOD levels of the tiles, and by changing the bounding box of the tiles, in order to optimize the LODs
*   applies ASOBO extension tags to the gltf files, in order to enable the road management and the collisions
*   fix gltf doublesided attributes, in order to remove texture flickering issues
*   removes the orphaned scenery object xml files (scenery object xml files that do not have associated gltf and/or bin files)
*   automatically rebuild the scenery package, if the MSFS SDK is correctly installed, and MSFS 2020 is not running
**
4) fix_tiles_altitudes script :  **  

4.1) Presentation:  
This script applies the CTD issues fix (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/)).  
When using the scenery_optimisation script, there are chances that the resulting tiles are slightly decaled in the x and/or y axis.  
This decal can easily be fixed by going into the MSFS SDK, open the project, click on the "Save scenery..." button to order the scenery objects by type, then select all the tiles (not the lights, rectangles or polygons, just the tiles) and move them to the appropriate location. But this move can break some tiles altitude.  
To fix it, save your scenery after moving the tiles to their appropriate location, then close your project and MSFS 2020, and run the fix_tile_altitudes script. Once the script has finished running and rebuidling your project, reopen the project in the MSFS SDK. The tiles position and altitude should now be correct.  

4.2) Installation:  
Just put the fix_tile_altitudes.py script, and the retrievepos.js script in a folder of your choice.  

4.3) Configuration:  
Change the following settings, according to your project:  

*   **projects_folder:** the parent folder that contains your sceneries
*   **project_name:** the name of your project
*   **node_js_folder**: the folder that contains the node js script that retrieves the Google Earth coords
*   **fspackagetool_folder**: the folder that contains the fspackagetool exe that builds the MSFS packages
*   **project_file_name**: the name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
*   **scene_file_name: **the name of the xml file that embeds the tile descriptions (by default, objects.xml)
*   **package_definitions_file_name**: the name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
*   **author_name**: the name of the author of the scenery
*   **build_package_enabled**: enable the package compilation when the script has finished (default is True)
*   **fix_with_googleEarthDecoder_data**: if set to True, tells the script to use the backup of the old objects.xml data (the one produced by the Google Earth Decoder tool) to fix tiles altitude. If set to False, tells the script to directly retrieve tiles altitude from the Google Earth API (default is True)

4.4) Usage:  
Open Blender **in administrator mode**.  
Go in the Scripting view, then click on the Open icon, and choose the fix_tile_altitudes python script.  
When the configuration is done, open the Blender system console Window (Window => Toggle System Console). Then, run the script.  
The fix comes with two methods: the default one uses the backup of the old objects.xml data (the one produced by the Google Earth Decoder tool)the other method tries to retrieve the altitude directly based on the Google Earth data (using the Google Earth API)  

4.5) Process:  

*   rename the modelLib folder, in order to fix CTD issues (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/))
*   if necessary, install the node Js xhr2 module (npm install xhr2)
*   retrieve objects positions from Google earth, via the Google Earth API, and put the results in .pos files corresponding to the scenery tiles
*   update the tiles altitude, using the backup objects.xml file, if fix_with_googleEarthDecoder_data is set to True, or using the .pos files generated by the Google Earth API, if fix_with_googleEarthDecoder_data is set to False
*   automatically rebuild the scenery package, if the MSFS SDK is correctly installed, and MSFS 2020 is not running
**
5) update_objects_LODs script: **  

5.1) Presentation:  
This script applies the CTD issues fix (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/)).  
This script automates the process of changing the LOD levels for all the tiles of a scenery.  

5.2) Installation:  
Just put the update_object_LODs.py script in a folder of your choice.  

5.3) Configuration:  
Change the following settings, according to your project:  

*   **projects_folder**: the parent folder that contains your sceneries
*   **project_name**: the name of your project
*   **target_lods**: an array representing the minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
*   **fspackagetool_folder**: the folder that contains the fspackagetool exe that builds the MSFS packages
*   **project_file_name**: the name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
*   **scene_file_name: **the name of the xml file that embeds the tile descriptions (by default, objects.xml)
*   **package_definitions_file_name**: the name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
*   **author_name**: the name of the author of the scenery
*   **build_package_enabled**: enable the package compilation when the script has finished (default is True)

5.4) Usage:  
Open Blender **in administrator mode**.  
Go in the Scripting view, then click on the Open icon, and choose the update_object_LODs python script.  
When the configuration is done, open the Blender system console Window (Window => Toggle System Console). Then, run the script.  

5.5) Process:  

*   rename the modelLib folder, in order to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
*   update the LOD levels for each tile in the tile_object_name.xml files
*   automatically rebuild the scenery package, if the MSFS SDK is correctly installed, and MSFS 2020 is not running
**
6) merge_sceneries script: **  

6.1) Presentation:  
This script applies the CTD issues fix (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/)).  
This script automates the process of merging a Google Earth Decoder source scenery into another Google Earth Decoder scenery.  

6.2) Installation:  
Just put the merge_sceneries.py script in a folder of your choice.  

6.3) Configuration:  
Change the following settings, according to your project:  

*   **projects_folder**: the parent folder that contains your sceneries
*   **src_project_name**: the name of the scenery that you want to include in the final scenery
*   **dest_project_name**: the name of the final project that should include both sceneries
*   **fspackagetool_folder**: the folder that contains the fspackagetool exe that builds the MSFS packages
*   **src_project_file_name**: the name of the xml file that embeds the source project definition (by default, src_project_name.xml or author_name+src_project_name.xml)
*   **dest_project_file_name**: the name of the xml file that embeds the destination project definition (by default, dest_project_name.xml or author_name+dest_project_name.xml)
*   **src_scene_file_name**: the name of the xml file that embeds the tile descriptions (by default, objects.xml) for the scenery that you want to include in the final scenery
*   **dest_scene_file_name**: the name of the xml file that embeds the tile descriptions (by default, objects.xml) for the final project that should include both sceneries
*   **src_package_definitions_file_name**: the name of the xml file that embeds the source package definitions (by default, src_project_name.xml or author_name+src_project_name.xml)
*   **dest_package_definitions_file_name**: the name of the xml file that embeds the destination package definitions (by default, dest_project_name.xml or author_name+dest_project_name.xml)
*   **author_name**: the name of the author of the scenery
*   **build_package_enabled**: enable the package compilation when the script has finished (default is True)

6.4) Usage:  
Open Blender **in administrator mode**.  
Go in the Scripting view, then click on the Open icon, and choose the update_object_LODs python script.  
When the configuration is done, open the Blender system console Window (Window => Toggle System Console). Then, run the script.  

6.5) Process:  

*   rename the modelLib folder, in order to fix CTD issues (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/))
*   backup the modelLib files of the final project that should include both sceneries, into a backup subfolder, so called merge_sceneries
*   copy all the xml files, gltf files, bin files and texture files from the source scenery to the destination scenery, overwritting the existing ones
*   update the destination scenery scene xml file (objects.xml by default) to change the tiles guid corresponding to the source scenery tiles
*   add the guid for the source tiles that does not exist in the destination scenery
*   automatically rebuild the scenery package, if the MSFS SDK is correctly installed, and MSFS 2020 is not running
**
7) clean_package_files script: **  

7.1) Presentation:  
This script applies the CTD issues fix (see [https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/](../../blog/creators-guide-fix-ctd-issues-on-your-scenery/)).  
This script automatically removes unused package files (.gltf, .bin and texture files), aka the files that are linked with tiles that have been removed from the scene. It appears that, if this cleaning is not done, the resulting package keep those files.  

7.2) Installation:  
Just put the clean_package_files.py script in a folder of your choice.  

7.3) Configuration:  
Change the following settings, according to your project:  

*   **projects_folder**: the parent folder that contains your sceneries
*   **project_name**: the name of your project
*   **fspackagetool_folder**: the folder that contains the fspackagetool exe that builds the MSFS packages
*   **project_file_name**: the name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
*   **scene_file_name: **the name of the xml file that embeds the tile descriptions (by default, objects.xml)
*   **package_definitions_file_name**: the name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
*   **author_name**: the name of the author of the scenery
*   **build_package_enabled**: enable the package compilation when the script has finished (default is True)

7.4) Usage:  
Open Blender** in administrator mode**.   
Go in the Scripting view, then click on the Open icon, and choose the clean_package_files python script.  
When the configuration is done, open the Blender system console Window (Window => Toggle System Console). Then, run the script.  

7.5) Process:  

*   rename the modelLib folder, in order to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
*   browse the scenery object xml files in the object folder
*   check the presence of the corresponding guid in the scene xml file
*   if the guid is not found in the scene xml file, remove the files associated with this scenery object xml file (.gltf, .bin, and texture files), in order to reduce the resulting package size
