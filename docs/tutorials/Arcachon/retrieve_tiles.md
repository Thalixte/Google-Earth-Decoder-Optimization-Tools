# 2. Retrieve the MSFS scenery photogrammetry tiles

![type:video](video.mp4){: src='../../../assets/videos/arcachon/download_tiles.mp4' .md-video}

* open the __[Google Earth Decoder][1]__ tool, and zoom to the Arcachon town.
* select the path to the Arcachon MSFS Project scenery folder, and navigate to the PackagesSources subfolder: here ==**F:\\MsfsProjects\\Arcachon\\PackageSources\\**==.
* deploy the `LOD OPTIONS` section, and select ==**17: 1,52 meters/texel**== as the min Lod Range, and ==**19: 38 centimeters/texel**== as the max Lod Range. Don't care about the LOD # minSize values.
!!! warning "Lod Range recommended values for GEDOT"

    I strongly recommend to select **17 as the min Lod Range value**, in order for GEDOT to work correctly.
    I also strongly recommend not to select **a max Lod value higher than 20**.
* deploy the `COLOR CORRECTION` section, and select the level for the Color Correction values. I personally recommend those settings, by [OjO][2]:  

<div class="row no-bottom-margin content-box" markdown="1">
  <div class="col-sm-4 text-center" markdown="1">
  
  | Color Correction |     Value     |
  |:-----------------|:-------------:|
  | `Red Level`      | **==1,00==**  |
  | `Green Level`    | **==0,95==**  |   
  | `Green Level`    | **==0,95==**  | 
  | `Blue Level`     | **==0,90==**  |
  | `Brightness`     | **==0,85==**  |
  | `Contrast`       | **==0,90==**  |
  | `Saturation`     | **==0,95==**  |
  | `Hue`            | **==1,00==**  |  

  </div>
  <div markdown="1" class="col-sm-7 text-center md-typeset__scrollwrap">
  ![google_earth_decoder_color_corrections.png](..%2F..%2Fassets%2Fimages%2Fgoogle_earth_decoder_color_corrections.png){ .text-center .container-fluid .img-fluid}
  </div>
  <div markdown="1" class="col-sm-1 text-center md-typeset__scrollwrap">
  </div>
</div>
* Click on the map (with the right mouse button) to select the top left corner of the area you want to download.  
  Then, keep the button clicked, and drag the selection to the right bottom of the area you want to download, like this:  

![google_earth_decoder_selection.png](..%2F..%2Fassets%2Fimages%2Fgoogle_earth_decoder_selection.png)  

*  Once the area selected, click on the ![google_earth_decoder_download_buttton.png](..%2F..%2Fassets%2Fimages%2Fgoogle_earth_decoder_download_buttton.png) button, then wait until the download has finished.

The resulting file tree of the Arcachon project is presented below:

```
Arcachon
│   Arcachon.ini
│   Arcachon.xml
│
├───backup
├───PackageDefinitions
│   │   thalixte-arcachon.xml
│   │
│   └───thalixte-arcachon
│       │   Business.json
│       │
│       └───ContentInfo
│               Thumbnail.jpg
│
└───PackageSources
    ├───modelLib
    │   │   21537373607263635.xml
    │   │   21537373607263635_LOD00.bin
    │   │   21537373607263635_LOD00.gltf
    │   │   21537373607263635_LOD01.bin
    │   │   21537373607263635_LOD01.gltf
    │   │   21537373607263635_LOD02.bin
    │   │   21537373607263635_LOD02.gltf
    │   │   21537373607263637.xml
    │   │   ...
    │   │   21537373625142405.xml
    │   │   21537373625142405_LOD00.bin
    │   │   21537373625142405_LOD00.gltf
    │   │   21537373625142405_LOD01.bin
    │   │   21537373625142405_LOD01.gltf
    │   │   21537373625142405_LOD02.bin
    │   │   21537373625142405_LOD02.gltf
    │   │
    │   └───texture
    │           21537373607263635_LOD00_0.png
    │           21537373607263635_LOD00_1.png
    │           21537373607263635_LOD00_10.png
    │           21537373607263635_LOD00_11.png
    │           21537373607263635_LOD00_12.png
    │           21537373607263635_LOD00_13.png
    │           21537373607263635_LOD00_14.png
    │           21537373607263635_LOD00_15.png
    │           21537373607263635_LOD00_16.png
    │           21537373607263635_LOD00_17.png
    │           21537373607263635_LOD00_18.png
    │           21537373607263635_LOD00_19.png
    │           21537373607263635_LOD00_2.png
    │           21537373607263635_LOD00_20.png
    │           21537373607263635_LOD00_21.png
    │           21537373607263635_LOD00_22.png
    │           21537373607263635_LOD00_23.png
    │           21537373607263635_LOD00_24.png
    │           21537373607263635_LOD00_3.png
    │           21537373607263635_LOD00_4.png
    │           21537373607263635_LOD00_5.png
    │           21537373607263635_LOD00_6.png
    │           21537373607263635_LOD00_7.png
    │           21537373607263635_LOD00_8.png
    │           21537373607263635_LOD00_9.png
    │           21537373607263635_LOD01_0.png
    │           21537373607263635_LOD01_1.png
    │           21537373607263635_LOD01_2.png
    │           21537373607263635_LOD01_3.png
    │           21537373607263635_LOD01_4.png
    │           21537373607263635_LOD01_5.png
    │           21537373607263635_LOD01_6.png
    │           21537373607263635_LOD01_7.png
    │           21537373607263635_LOD02_0.png
    │           21537373607263635_LOD02_1.png
    │           ...
    │           21537373625142405_LOD00_0.png
    │           21537373625142405_LOD00_1.png
    │           21537373625142405_LOD00_10.png
    │           21537373625142405_LOD00_11.png
    │           21537373625142405_LOD00_12.png
    │           21537373625142405_LOD00_13.png
    │           21537373625142405_LOD00_14.png
    │           21537373625142405_LOD00_15.png
    │           21537373625142405_LOD00_2.png
    │           21537373625142405_LOD00_3.png
    │           21537373625142405_LOD00_4.png
    │           21537373625142405_LOD00_5.png
    │           21537373625142405_LOD00_6.png
    │           21537373625142405_LOD00_7.png
    │           21537373625142405_LOD00_8.png
    │           21537373625142405_LOD00_9.png
    │           21537373625142405_LOD01_0.png
    │           21537373625142405_LOD01_1.png
    │           21537373625142405_LOD01_2.png
    │           21537373625142405_LOD01_3.png
    │           21537373625142405_LOD02.png
    │
    └───scene
            objects.xml
```


[1]:https://drive.google.com/u/0/uc?id=18zdIjLbRgM5Ce1PtFPKYn-bCfOZcpPAO&export=download
[2]:https://flightsim.to/profile/OjO