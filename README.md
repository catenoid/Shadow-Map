Shadow-Map
==========

LIDAR GIS Monte Carlo calculation of shadowed areas based on python ephum sun positioning

Using ![LIDAR](https://en.wikipedia.org/wiki/Lidar) height map data, we can predict how the sun's light will be blocked for a given time of day. This script chooses random samples of the map, and treats each sample like a sundial, tracing the projection of the sample across the geographic region (based on the sun's direction at a specified time and date). A point is "shadowed" (coloured black in the pictures below) if this projection is taller than the building height at that point. The algorithm has potential applications in urban solar panel placement, calculating which rooftops can most capitalise on good sun exposure.

The height map data is expected in ESRI ASCII raster format; this sample data set for postcode OX13BW came from the Geomatics Group used under a non-commercial license. When this code was written in early 2014, LIDAR data sets were not open data, but available for free to academics. After September 2015, LIDAR datasets for England were released as [open data](http://us6.campaign-archive2.com/?u=e7311d49e9ac144a359ee2a96&id=ce444955ae) by the Environment Agency.

Example maps
------------

9999 samples at 10 am
![9999 samples](https://camo.githubusercontent.com/0ee2adafe7480b53f551b0dc9bef73853ae73cd4/687474703a2f2f692e696d6775722e636f6d2f38713233714a552e706e67)
99999 samples at 10 am 
![99999 samples](https://camo.githubusercontent.com/743d27135187210eb3e0eee4617c10761d3bc79c/687474703a2f2f692e696d6775722e636f6d2f67305275326b322e706e67)
999999 samples at 10 am
![999999 samples](https://camo.githubusercontent.com/3cd6ade83630b73b1a0aa4fd6c3d831c4cf686d3/687474703a2f2f692e696d6775722e636f6d2f79454b35796b622e706e67)
