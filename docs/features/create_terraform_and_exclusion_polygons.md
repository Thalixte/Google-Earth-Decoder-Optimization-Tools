# Create the terraform and exclusion polygons for the MSFS scenery project

Once the photogrammetry tiles have been optimized, GEDOT can automatically generate the terraform and exclusion polygons for the project.

!!! info "Exclusion polygons"

    GEDOT produces two types of exclusion polygons:  

    * exclusion building polygons: exclude the [Blackshark.ai][1] generated buildings to avoid conflicts between those AI buildings and the photogrammetry ones.  
    * exclusion vegetation polygons: preserve coastal aspects (beaches, shores), thanks to vegetation exclusions polygons that cover the water and the shores.

!!! info "Terraform polygons"

    The terraform polygons are created, but not enabled. When enabled, they can be used to fix some specific z-fighting issues between the MSFS original ground, and the photogrammetry tile surface.

All you have to do is to select `Google Earth Decoder Optimization Tools` > `3. Create the terraform and exclusion polygons for the scenery` in the top menu.

![type:video](video.mp4){: src='../assets/videos/arcachon/create_terraform_and_exclusion_polygons.mp4' .md-video}

## Set up the creation of terraform and exclusion polygons for the project
 
* (optional) indicate the name of the city where the airport is located in the field `Airport city` (ex.: ==**Arcachon**==). You can also use an [OSM][3] Geocode definition for the airport: (ex.: ==**Santos Dumont Airport, Rio de Janeiro**==). This information is necessary to exclude the airport area from the polygons.

!!! question "What is an [OSM][3] Geocode ?"

    An [OSM][3] Geocode is a litteral designation of an [OSM][3] object or an [OSM][3] relation (a geocode ID). It can be a specific location (for instance: Buckingham Palace, London), or a city (for instance Arcachon, France). It relies on the [Nominatim][2] (from the Latin, 'by name') tool for [OpenStreetMap][3].

## Run the polygons generation process

If all the settings are correctly set, the [Create the terraform and exclusion polygons for the scenery...](javascript:void(0)){ .md-button .gedot } button should be  enabled (except if the [MSFS][2] project folder does not exist, has been renamed or removed).  
Just click on this button, and a [Blender][1] window console will appear on the screen.

Once finished, you should see this on the console:   
![create_terraform_and_excludion_polygons.png](..%2Fassets%2Fimages%2Fcreate_terraform_and_excludion_polygons.png){ align=center }   

By default, the building process is executed by the MSFS fspackagetool exe. At the end of the process, you should see this window:

![fspackagetools_build_completed_after_polygons_generation.png](..%2Fassets%2Fimages%2Ffspackagetools_build_completed_after_polygons_generation.png)

## Generated files

### .shp files

When GEDOT process the automatic generation of the terraform and exclusion polygons, it downloads [OpenStreetMap][3] ([OSM][3]) data and store them in several file in shapefile format. Those files are located in the shp subfolder of the project:

```
Arcachon
└───shp
        aeroway.shp
        amenity.cpg
        amenity.dbf
        amenity.prj
        amenity.shp
        amenity.shx
        boundary.cpg
        boundary.dbf
        boundary.prj
        boundary.shp
        boundary.shx
        building.cpg
        building.dbf
        building.prj
        building.shp
        building.shx
        construction.cpg
        construction.dbf
        construction.prj
        construction.shp
        construction.shx
        grass.cpg
        grass.dbf
        grass.prj
        grass.shp
        grass.shx
        highway.cpg
        highway.dbf
        highway.prj
        highway.shp
        highway.shx
        industrial.cpg
        industrial.dbf
        industrial.prj
        industrial.shp
        industrial.shx
        landuse.cpg
        landuse.dbf
        landuse.prj
        landuse.shp
        landuse.shx
        man_made.cpg
        man_made.dbf
        man_made.prj
        man_made.shp
        man_made.shx
        natural.cpg
        natural.dbf
        natural.prj
        natural.shp
        natural.shx
        natural_water.cpg
        natural_water.dbf
        natural_water.prj
        natural_water.shp
        natural_water.shx
        nature_reserve.shp
        park.cpg
        park.dbf
        park.prj
        park.shp
        park.shx
        pitch.cpg
        pitch.dbf
        pitch.prj
        pitch.shp
        pitch.shx
        railway.cpg
        railway.dbf
        railway.prj
        railway.shp
        railway.shx
        residential.cpg
        residential.dbf
        residential.prj
        residential.shp
        residential.shx
        rocks.shp
        sea.cpg
        sea.dbf
        sea.prj
        sea.shp
        sea.shx
        wall.cpg
        wall.dbf
        wall.prj
        wall.shp
        wall.shx
        water.cpg
        water.dbf
        water.prj
        water.shp
        water.shx
        waterway.cpg
        waterway.dbf
        waterway.prj
        waterway.shp
        waterway.shx
```
The first time, retrieving those data can take some times, depending on the size of the area, and the complexity of the [OSM][3] data.  
Once those data are downloaded and stored in a .shp file, they are not downloaded again (the shp folder acts as a cache).

Here is a visualization of the retrieved OSM data, using the [BlenderGIS addon][9]:
<figure class="md-blender" markdown="1">
  ![arcachon_osm_data.png](..%2Fassets%2Fimages%2Farcachon_osm_data.png)
  <figcaption>OSM data visualization for Arcachon city</figcaption>
</figure>


### .osm files

Based on those [OSM][3] data, osm files are generated in the osm folder. Those are the processed files used to create the polygons in the MSFS scenery definition file (for instance arcachon.xml):

```
Arcachon
└───osm
        amenity_terraform_polygons.osm
        bbox_21537373607263635.osm
        bbox_21537373607263637.osm
        ...
        bbox_21537373625140426.osm
        bbox_21537373625140604.osm
        bbox_exclusion.osm
        construction_terraform_polygons.osm
        exclusion.osm
        exclusion_building_polygons.osm
        exclusion_vegetation_polygons.osm
        industrial.osm
        industrial_terraform_polygons.osm
        pitch_terraform_polygons.osm
```

The .osm files used to generate exclusion and terraform polygons are those ones:  

* **amenity_terraform_polygons.osm**: used to create [amenity][4] terraform polygons, for [amenity area][4]. It is the top-level [OSM][3] tag describing useful and important facilities for visitors and residents, such as toilets, telephones, banks, pharmacies, prisons and schools.
* **construction_terraform_polygon.osm**: used to create [construction][5] terraform polygons, for [construction area][5]. It is the top-level [OSM][3] tag describing a geographical entity which is currently under construction.
* **industrial_terraform_polygons.osm**: used to create [industrial][6] terraform polygons, for [industrial area][6]. It delimits areas of land used for industrial purposes.
* **pitch_terraform_polygon.osm**: used to create [pitch][7] terraform polygons, for [pitches][7]. It describes an area designed for practising a particular sport, normally designated with appropriate markings. Examples include tennis courts, basketball courts, ball parks, and riding arenas.
* **exclusion_building_polygons.osm**: used to create building exclusion polygons in order to avoid conflicts between AI generated buildings and photogrammetry buildings.
* **exclusion_vegetation_polygons.osm**: used to create vegetation exclusion polygons in order to avoid vegetation on the water and in the shores.

Those polygons can be opened in [Blender][8], by using the [BlenderGIS addon][9] (which is automatically installed by GEDOT, if not present in the [Blender][8] addons):
<figure class="md-blender" markdown="1">
  ![terraform_polygons.png](..%2Fassets%2Fimages%2Fterraform_polygons.png)
  <figcaption>Terraform polygons for Arcachon city (in yellow)</figcaption>
</figure>
<figure class="md-blender" markdown="1">
  ![exclusion_buidlings_polygons.png](..%2Fassets%2Fimages%2Fexclusion_buidlings_polygons.png)
  <figcaption>Exclusion buildings polygons for Arcachon city (in yellow)</figcaption>
</figure>
<figure class="md-blender" markdown="1">
  ![exclusion_vegetation_polygons.png](..%2Fassets%2Fimages%2Fexclusion_vegetation_polygons.png)
  <figcaption>Exclusion vegetation polygons for Arcachon city (in yellow)</figcaption>
</figure>

## Result in MSFS

Open MSFS, go to the scenery location, start a new flight, then enter the dev mode, and open the MSFS scenery project (by selecting the scenery xml file).

In the scenery Editor window, you can see that new groups have been created:  

* **GEDOT_generated_amenity_terraform_polygon:** contains all the [amenity][4] terraform polygons:  

![MSFS_arcachon_amenity_terraform_polygons.png](..%2Fassets%2Fimages%2FMSFS_arcachon_amenity_terraform_polygons.png)
* **GEDOT_generated_construction_terraform_polygon:** contains all the [construction][5] terraform polygons: 

![MSFS_arcachon_construction_terraform_polygons.png](..%2Fassets%2Fimages%2FMSFS_arcachon_construction_terraform_polygons.png)

* **GEDOT_generated_industrial_terraform_polygon:** contains all the [industrial][6] terraform polygons: 

![MSFS_arcachon_industrial_terraform_polygons.png](..%2Fassets%2Fimages%2FMSFS_arcachon_industrial_terraform_polygons.png)

* **GEDOT_generated_pitch_terraform_polygon:** contains all the [pitch][7] terraform polygons:  

![MSFS_arcachon_pitch_terraform_polygons.png](..%2Fassets%2Fimages%2FMSFS_arcachon_pitch_terraform_polygons.png)

* **GEDOT_exclusion_building_terraform_polygon:** contains all the exclusion building terraform polygons:    

![MSFS_arcachon_exclusion_buildings_polygons.png](..%2Fassets%2Fimages%2FMSFS_arcachon_exclusion_buildings_polygons.png)

* **GEDOT_exclusion_vegetation_terraform_polygon:** contains all the exclusion vegetation terraform polygons: 

![MSFS_arcachon_exclusion_vegetation_polygons.png.png](..%2Fassets%2Fimages%2FMSFS_arcachon_exclusion_vegetation_polygons.png.png)

Another way to check for the generated exclusion polygons is to use the `debug` > `terrain` > `Exclusion debug` tool:  

![MSFS_arcachon_debug_terrain.png](..%2Fassets%2Fimages%2FMSFS_arcachon_debug_terrain.png)


[1]:https://blackshark.ai/
[2]:https://nominatim.openstreetmap.org/ui/search.html
[3]:https://www.openstreetmap.org/
[4]:https://wiki.openstreetmap.org/wiki/Key:amenity
[5]:https://wiki.openstreetmap.org/wiki/Key:construction
[6]:https://wiki.openstreetmap.org/wiki/Tag:landuse%3Dindustrial
[7]:https://wiki.openstreetmap.org/wiki/Tag:leisure%3Dpitch
[8]:https://www.blender.org/
[9]:https://github.com/domlysz/BlenderGIS