# Project Overview
* This tool automates creation of slope profiles for hiking trails.
* Each trail is split into multiple segments of 10 meters maximum length per segment (default).
* Using a Digital Elevation Model (DEM), elevation is extracted for every vertex in the split trails file.
* Extracted elevation is processed with the Field Calculator to assign a slope value for every segment.
* The python script was built using the Processing Modeler in QGIS Desktop 3.10.4 with GRASS 7.8.2.
---
# Required Input Files
* Shape file (lines) of trails. [Available here.](http://wvgis.wvu.edu/data/dataset.php?ID=413)
* DEM of the area of interest. The higher the resolution, the better. Mine is 1-3 meters. [Available here.](http://wvgis.wvu.edu/data/dataset.php?ID=477)
---
# Results

![Image of map](https://github.com/jstnhllrd/trail_slope_project/blob/main/vf_2MP.png)
##### Map of the primary hiking trails at Valley Falls State Park, WV.

&nbsp;

![Image of map](https://github.com/jstnhllrd/trail_slope_project/blob/main/slope_example_10m_2MP.png)
##### Trail slopes map of Valley Falls State Park, WV. The trails were split into, maximum, 10 meter segments.

&nbsp;

![Image of map](https://github.com/jstnhllrd/trail_slope_project/blob/main/slope_example_50m_2MP.png)
##### Trail slopes map of Valley Falls State Park, WV. The trails were split into, maximum, 50 meter segments.
---
# Conclusions

The decision for segment length will vary by your individual needs and data available. The end goal is that the map is useful.
I like the 50 meter version because it smooths over a lot of the variation.

---
## Resources

The overall approach for this analysis is borrowed from a [Stack Exchange post.](https://gis.stackexchange.com/questions/165683/how-do-i-find-the-slope-of-road-segments-with-point-elevation-data-of-the-same-l) I would encourage you to check it out if you're interested in doing this.
