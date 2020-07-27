# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:35:30 2020

@author: Reza
"""

import math

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    coordinate_limit = [lat1 >= -90,
                        lat1 <= 90,
                        lat2 >= -90,
                        lat2 <= 90,
                        lon1 >= -180,
                        lon1 <= 180,
                        lon2 >= -180,
                        lon2 <= 180]

        #if (lat1 >= -90 and lat1 <= 90) and (lat2 >= -90 and lat2 <= 90) 
    if all(coordinate_limit):
        radius = 6371 # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
    else:
        d = math.nan
    
    return d
        

if __name__ == "__main__":
    print("distance between (3.213979,101.638397) and (3.227013,101.637439) is: {0:.2f} km".format(distance((93.213979,101.638397), (3.227013,101.637439))))