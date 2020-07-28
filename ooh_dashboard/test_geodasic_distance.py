# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 04:04:30 2020

@author: Reza
"""

from point_distance import geodasic_distance, euclidean_distance

def test_distance_1():
    assert(geodasic_distance((3.213979,101.638397), (3.227013,101.637439)) == 1.4532)
    
def test_distance_2():
    assert(geodasic_distance((3.213979,101.638397), (3.133282,101.707324)) == 11.7932)
    
def test_distance_3():
    assert(euclidean_distance((0, 4), (3, 0)) == 5)
    
def test_distance_4():
    assert(euclidean_distance((0, 5), (12, 0)) == 13)