# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:35:30 2020

@author: Reza
"""

import math

def distance(origin, destination):
    lat_1, lon_1 = origin
    lat_2, lon_2 = destination
    radius = 6371 # km
    
    coordinate_limit = [lat_1 >= -90,
                        lat_1 <= 90,
                        lat_2 >= -90,
                        lat_2 <= 90,
                        lon_1 >= -180,
                        lon_1 <= 180,
                        lon_2 >= -180,
                        lon_2 <= 180]

        #if (lat1 >= -90 and lat1 <= 90) and (lat2 >= -90 and lat2 <= 90) 
    if all(coordinate_limit):
        dlat = math.radians(lat_2-lat_1)
        dlon = math.radians(lon_2-lon_1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat_1)) \
            * math.cos(math.radians(lat_2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        delta = round(radius * c, 4)
    else:
        delta = math.nan
    
    return delta