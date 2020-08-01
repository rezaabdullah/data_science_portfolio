# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:37:48 2020

@author: Reza
"""

from pointdistance import GeodesicPoints
from pointdistance import EuclideanPoints
from math import nan

def test_EuclideanPoints():
    euclideanPoints = EuclideanPoints((0, 3), (4, 0))
    assert(euclideanPoints.distance == 5)