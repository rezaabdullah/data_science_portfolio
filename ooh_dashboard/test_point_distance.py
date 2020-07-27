# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 04:04:30 2020

@author: Reza
"""

from point_distance import distance

def test_distance_1():
    assert(distance((3.213979,101.638397), (3.227013,101.637439)) == 1.4532)
    
def test_distance_2():
    assert(distance((3.213979,101.638397), (3.133282,101.707324)) == 11.7932)