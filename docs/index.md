## What is GEDOT ?

GEDOT (for Google Earth Decoder Optimization Tools) is a [Blender][1]{:target="_blank"} Addon which aims at 
providing a bunch of tasks to ease the process of integrating photogrammetry data retrieved with the Google Earth Decoder Tool 
into [Microsoft Flight Simulator&copy; 2020](https://www.flightsimulator.com/){:target="_blank"} \.  

Because it is a [Blender][1]{:target="_blank"} addon, this tool is written in [python](https://www.python.org/){:target="_blank"} (v3.10).

## GEDOT main features

* initialize a new MSFS 2020 scenery project structure
* optimize the downloaded tiles in order to keep reasonable framerate while flying over the scenery
* generate automatically exclusion building polygons, as well as exclusion vegetation polygons, and some extra terraforming polygons, using [OpenStreetMap (OSM)][2]{:target="_blank"} data
* remove unnecessary vertices (water vertices, vegetation vertices), using [OpenStreetMap (OSM)][2] data
* generate automatically 10m DEM data for each tile, based on the tile's 3d data, and [OpenStreetMap (OSM)][2]{:target="_blank"} data
* add a collider for each tile of the scenery, in order to optimize the CPU resources for collision detection and road traffic
* reduce the texture memory footprint by compressing them in DDS non-transparent format
* generate automatically landmark location from an [OSM][2]{:target="_blank"} geocode
* generate automatically lights around a specific location, using [OSM][2]{:target="_blank"}  geocode, or [OSM][2]{:target="_blank"} id
* remove automatically a specific location from the tiles, using [OSM][2]{:target="_blank"}  geocode, or [OSM][2]{:target="_blank"} id
* isolate automatically a specific location from the tiles, using [OSM][2]{:target="_blank"}  geocode, or [OSM][2]{:target="_blank"} id
* ... and some extra specific features  
      

!!! warning "Theme extension prerequisites"

    As the [`custom_dir`][custom_dir] setting is used for the theme extension
    process, Material for MkDocs needs to be installed via `pip` and referenced
    with the [`name`][name] setting in `mkdocs.yml`. It will not work when
    cloning from `git`.


[1]:https://www.blender.org/
[2]:https://www.openstreetmap.org/