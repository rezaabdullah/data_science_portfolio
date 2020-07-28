# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:37:48 2020

@author: Reza
"""

from point_distance import EuclideanPoints, GeodesicPoints

euclideanDistance = EuclideanPoints((0,3), (4,0))
print(euclideanDistance.distance)
geodesicDistance = GeodesicPoints((3.213979,101.638397), (3.22724,101.637501))
print(geodesicDistance.distance)