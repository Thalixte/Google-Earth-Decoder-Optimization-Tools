# Presentation

<p class="md-badges">
<a href="https://hits.seeyoufarm.com" target="_blank"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FThalixte%2FGoogle-Earth-Decoder-Optimization-Tools&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true" class="md-badge"/></a>
<img src="https://img.shields.io/github/license/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/v/release/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/stars/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/forks/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">
<img src="https://img.shields.io/github/issues/Thalixte/Google-Earth-Decoder-Optimization-Tools?style=flat-square" class="md-badge">


</p>

## What is GEDOT ?

GEDOT (for Google Earth Decoder Optimization Tools) is a [Blender][1] Addon which aims at 
providing a bunch of tasks to ease the process of integrating photogrammetry data retrieved with the Google Earth Decoder Tool 
into [Microsoft Flight Simulator&copy; 2020](https://www.flightsimulator.com/) \.  

Because it is a [Blender][1] addon, this tool is written in [python](https://www.python.org/) (v3.10).

## GEDOT main features

* initialize a new MSFS 2020 scenery project structure
* optimize the downloaded tiles in order to keep reasonable framerate while flying over the scenery
* generate automatically exclusion building polygons, as well as exclusion vegetation polygons, and some extra terraforming polygons, using [OpenStreetMap (OSM)][2] data
* remove unnecessary vertices (water vertices, vegetation vertices), using [OpenStreetMap (OSM)][2] data
* generate automatically 10m DEM data for each tile, based on the tile's 3d data, and [OpenStreetMap (OSM)][2] data
* add a collider for each tile of the scenery, in order to optimize the CPU resources for collision detection and road traffic
* reduce the texture memory footprint by compressing them in DDS non-transparent format
* generate automatically landmark location from an [OSM][2] geocode
* generate automatically lights around a specific location, using [OSM][2]  geocode, or [OSM][2] id
* remove automatically a specific location from the tiles, using [OSM][2]  geocode, or [OSM][2] id
* isolate automatically a specific location from the tiles, using [OSM][2]  geocode, or [OSM][2] id
* ... and some extra specific features  

[1]:https://www.blender.org/
[2]:https://www.openstreetmap.org/