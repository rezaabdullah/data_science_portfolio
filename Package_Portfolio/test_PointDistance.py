# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:37:48 2020

@author: Reza
"""

from point-distance import PointDistance
from math import nan

class testGeodesicPointsClass:
    def setup(self):
        self.Points((3.213979,101.638397), (3.227013,101.637439))
        self.GeodesicPoints((93.213979,101.638397), (3.227013,101.637439))

        def test_initialization(self):
            assert(self.Points.coordinate_1 == (3.213979,101.638397))
            assert(self.Points.distance == nan)