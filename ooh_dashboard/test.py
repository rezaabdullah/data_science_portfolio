# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 04:04:30 2020

@author: Reza
"""

from point_distance import distance

distance_km = distance((3.213979,101.638397), (3.227013,101.637439))
assert(distance_km == 1.4532)
print("distance between (3.213979,101.638397) and (3.227013,101.637439) is: {0:.2f} km, correct answer is 1.4532 km".format(distance_km))