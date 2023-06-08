# Cleanup the 3d data from the photogrammetry tiles

When the photogrammetry tiles have been optimized, it is now possible to cleanup their 3d data, i.e. remove 3d data that can interfere with the MSFS generated 3d assets, mainly the water area and the vegetation area.

All you have to do is to select `Google Earth Decoder Optimization Tools` > `4. Cleanup 3d data fro Google Earth tiles` in the top menu.

![type:video](video.mp4){: src='../assets/videos/arcachon/cleanup_3d_data_accurate.mp4' .md-video}

## Set up the cleanup of the 3d data

First of all, you have to decide the method you will use to cleanup the 3d data.
Those methods rely on the accuracy of the [OpenStreetMap][1] data. Two levels of accuracy are available: **Accurate** and **Not accurate**.

### Check for [OpenStreetMap][1] data accuracy

* If you indicate to GEDOT that the [OpenStreetMap (OSM)][1] 3d data are accurate, GEDOT will use a constructive method to cleanup the data: this means that GEDOT will keep only the relevant data from the tiles (for instance, buildings and roads).  
* If you indicate to GEDOT that the [OpenStreetMap (OSM)][1] 3d data are not accurate, GEDOT will use a destructive method to cleanup the data: starting from the complete tile, it will remove the non relevant 3d data (for instance, forests, woods, sea, lake, ...)

!!! question "Why does the accuracy of [OSM][1] data determine the method that GEDOT uses to cleanup the 3d data ?"

    To be able to keep only the relevant 3d data (constructive method), GEDOT needs to know the shape of the buidlings in [OpenStreetMap][1].   
    When the [OSM][1] data are accurate, this means that almost all the buidlings (more than 95%) are represented in the OpenStreetMap area.

    If it is not the case (remember that [OpenStreetMap][1] is an open source project, based on the users' contributions), GEDOT cannot know the 3d data to keep. So the logic behind needs to be different. In this case, GEDOT uses a destructive method to remove the area that it can retrieve from the [OSM][1] data (water, forests, woods, etc...).

!!! question "How can i check for [OpenStreetMap][1] data accuracy ?"

    Open your Internet browser, and just ask this on the research bar: "_Your town_ OSM relation" (for instance, "==**Arcachon OSM relation**=="). Click on the first link proposed (this should be "Relation: _Your town_ (########)", for instance "==**Relation: Arcachon (1665459)**==")

    An example is provided here:
    ![type:video](video.mp4){: src='../assets/videos/arcachon/arcachon_check_for_osm_data.mp4' .md-video}

    Now, you can check for the accuracy of the OpenStreetMap data, and especially if the building shapes are mostly all available (in the case of Arcachon city, the 3d data are accurate, because they rely on cadastral data).

Here is an example of a city with accurate [OpenStreetMap][1] data ([Rotterdam][2]):

![rotterdam_osm_data.png](..%2Fassets%2Fimages%2Frotterdam_osm_data.png)

Here is an example of a city with not accurate [OpenStreetMap][1] data ([Rio de Janeiro][3]):

![rio_de_janeiro_osm_data.png.png](..%2Fassets%2Fimages%2Frio_de_janeiro_osm_data.png.png)

You see the difference ? In the [Rotterdam][2] 3d data, all the buildings are drawn (dark grey shapes), which is not the case in the [Rio de Janeiro][3] area.


### select the cleanup settings

Once you have decided the accuracy of the [OpenStreetMap][1] data, you can setup the cleanup process:  

* select the accuracy of the [OpenStreetMap][1] data in the list `OpenStreetMap accuracy`. Values are **Accurate** / **Not accurate**

* by default, GEDOT processes all the tiles that have not been cleaned yet. You can choose to process all the tiles (even those that have already be cleaned) by ticking the `Process all the tiles` checkbox

* (optional) indicate the name of the city where the airport is located in the field `Airport city` (ex.: ==**Arcachon**==). You can also use an [OSM][3] Geocode definition for the airport: (ex.: ==**Santos Dumont Airport, Rio de Janeiro**==). This information is necessary to exclude the airport photogrammetry data, if they exist

##### If you select "Accurate" in the list:
* the checkbox `Keep buildings 3d data` is readonly and is automatically checked   

* (optional) if you want to keep photogrammetry roads, tick the `Keep roads 3d data` checkbox (enabled by default)

* (optional) if you want to keep the construction area (which can be useful if the data between the photogrammetry and OpenStreetMap are not up-to-date), tick the `Keep construction area 3d data` checkbox

* (optional) if you want to keep residential and industrial area, without worrying about the real shapes of the buildings, tick the  `Keep residential and industrial area 3d data`.   
  This is useful in the case when not all the buildings are drawn in [OSM][1], but the residential and industrial area are clearly shaped (with the OSM tag landuse=residential and the OSM tag landuse=industrial).   
  It is a way of using the constructive method, even if the [OSM][1] data are not accurate. You can see an example of this type of OSM data accuracy in the [Cardiff city suburbs][4] (light grey area have the tag landuse=residential, whereas dark grey shapes represent the buildings):

![cardiff_suburbs_osm_data.png](..%2Fassets%2Fimages%2Fcardiff_suburbs_osm_data.png)

##### If you select "Not accurate" in the list:
* the checkbox `Exclude water 3d data` is readonly and is automatically checked

* (optional) if you want to exclude forests 3d data, tick the `Exclude forests 3d data` checkbox (it roughly corresponds to the [OSM][1] tag landuse=forest)

* (optional) if you want to exclude woods 3d data, tick the `Exclude woods 3d data` checkbox (it roughly corresponds to the [OSM][1] tag natural=wood)

* (optional) if you want to exclude other ground 3d data, tick the `Exclude other ground 3d data (farmlands, allotments, meadows, orchards)` checkbox

* (optional) if you want to exclude nature reserves 3d data, tick the `Exclude nature reserves 3d data` checkbox (it roughly corresponds to the [OSM][1] tag leisure=nature_reserve)

* (optional) if you want to exclude parks 3d data, tick the `Exclude parks 3d data` checkbox (it roughly corresponds to the [OSM][1] tag leisure=park)

## Run the cleanup process

If all the settings are correctly set, the [Cleanup 3d data from Google Earth tiles](javascript:void(0)){ .md-button .gedot } button should be  enabled (except if the [MSFS][6] project folder does not exist, has been renamed or removed).  
Just click on this button, and a [Blender][5] window console will appear on the screen.

Once finished, you should see this on the console:   
![cleanup_3d_data_from_photogrammetry_tiles.png](..%2Fassets%2Fimages%2Fcleanup_3d_data_from_photogrammetry_tiles.png){ align=center }   

By default, the building process is executed by the MSFS fspackagetool exe. At the end of the process, you shoud see this window:

![fspackagetools_build_completed_after_polygons_generation.png](..%2Fassets%2Fimages%2Ffspackagetools_build_completed_after_3d_data_cleanup.png)


!!! warning "cleanup 3d data backup folder"

    The first time the cleanup process is launched on a MSFS project, a new backup folder, named "cleanup_3d_data" is created:  
    ```command
    Arcachon
    └───backup
        └───cleanup_3d_data
            └───PackageSources
                ├───arcachon-modelLib
                │   └───texture
                └───scene
    ```
    This folder must be kept in order to run the process again, as it contains all the entire photogrammetry tiles (before the cleanup).  
    The cleanup process will always rely on those entire tiles. If the folder is deleted, and the process is executed again, it will take the already cleaned tiles, which can produce undesired results.

## Result

<div class="img-container" markdown="1">
  <div class="img background-img"></div>
  <div class="img foreground-img"></div>
  <input type="range" min="1" max="100" value="50" class="img-slider" name="img-slider" id="img-slider">
  <div class='img-slider-button'></div>
</div>


[1]:https://www.openstreetmap.org/
[2]:https://www.openstreetmap.org/relation/324431#map=15/51.9025/4.4649
[3]:https://www.openstreetmap.org/relation/57963#map=15/-22.8798/-43.2774
[4]:https://www.openstreetmap.org/relation/1625787#map=16/51.5063/-3.2129
[5]:https://www.blender.org/
[6]:https://www.flightsimulator.com/