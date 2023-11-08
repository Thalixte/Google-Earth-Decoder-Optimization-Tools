# Create the terraform and exclusion polygons for the MSFS scenery project

![type:video](video.mp4){: src='../../../assets/videos/arcachon/create_terraform_and_exclusion_polygons.mp4' .md-video}

## Set up the creation of terraform and exclusion polygons for the project
 
* indicate the name of the city where the airport is located in the field `Airport city`: here ==**Arcachon**==.  
This information is necessary to exclude the airport area from the polygons.

## Run the polygons generation process

Click on this button, and a [Blender][1] window console will appear on the screen.

Once finished, you should see this on the console:   
![create_terraform_and_excludion_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2Fcreate_terraform_and_excludion_polygons.png){ align=center }   

By default, the building process is executed by the MSFS fspackagetool exe. At the end of the process, you should see this window:

![fspackagetools_build_completed_after_polygons_generation.png](..%2F..%2F..%2Fassets%2Fimages%2Ffspackagetools_build_completed_after_polygons_generation.png)

## Result in MSFS

Open MSFS, go to the scenery location, start a new flight, then enter the dev mode, and open the MSFS scenery project (by selecting the scenery xml file).

In the scenery Editor window, you can see that new groups have been created:  

* **GEDOT_generated_amenity_terraform_polygon:** contains all the [amenity][4] terraform polygons:  

![MSFS_arcachon_amenity_terraform_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_amenity_terraform_polygons.png)

* **GEDOT_generated_construction_terraform_polygon:** contains all the [construction][5] terraform polygons: 

![MSFS_arcachon_construction_terraform_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_construction_terraform_polygons.png)

* **GEDOT_generated_industrial_terraform_polygon:** contains all the [industrial][6] terraform polygons: 

![MSFS_arcachon_industrial_terraform_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_industrial_terraform_polygons.png)

* **GEDOT_generated_pitch_terraform_polygon:** contains all the [pitch][7] terraform polygons:  

![MSFS_arcachon_pitch_terraform_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_pitch_terraform_polygons.png)

* **GEDOT_exclusion_building_terraform_polygon:** contains all the exclusion building terraform polygons:    

![MSFS_arcachon_exclusion_buildings_polygons.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_exclusion_buildings_polygons.png)

* **GEDOT_exclusion_vegetation_terraform_polygon:** contains all the exclusion vegetation terraform polygons: 

![MSFS_arcachon_exclusion_vegetation_polygons.png.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_exclusion_vegetation_polygons.png.png)

Another way to check for the generated exclusion polygons is to use the `debug` > `terrain` > `Exclusion debug` tool:  

![MSFS_arcachon_debug_terrain.png](..%2F..%2F..%2Fassets%2Fimages%2FMSFS_arcachon_debug_terrain.png)


[1]:https://blackshark.ai/
[2]:https://nominatim.openstreetmap.org/ui/search.html
[3]:https://www.openstreetmap.org/
[4]:https://wiki.openstreetmap.org/wiki/Key:amenity
[5]:https://wiki.openstreetmap.org/wiki/Key:construction
[6]:https://wiki.openstreetmap.org/wiki/Tag:landuse%3Dindustrial
[7]:https://wiki.openstreetmap.org/wiki/Tag:leisure%3Dpitch
[8]:https://www.blender.org/
[9]:https://github.com/domlysz/BlenderGIS