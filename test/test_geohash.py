# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 20:53:00 2017

@author: Alessandro Adamo
"""
import unittest
from gea.geohash import *


class TestGeoHash(unittest.TestCase):

    def test_encode(self):
        location = {'lat': 41.890251, 'lon': 12.492373}
        self.assertEqual(geohash_encode(location, 5), 'sr2yk')
        self.assertEqual(geohash_encode(location, 6), 'sr2yk3')

    def test_bounds(self):
        self.assertEqual(geohash_bounds('sr2yk'), {'sw': {'lat': 41.8798828125, 'lon': 12.48046875}, 'ne': {'lat': 41.923828125, 'lon': 12.5244140625}})

    def test_decode(self):
        self.assertEqual(geohash_decode('sr2yk3bsm'), {'lat': 41.890247, 'lon': 12.492378})

    def test_adjacent(self):
        self.assertEqual(geohash_adjacent('sr2yk3bsm', 'n'), 'sr2yk3bst')
        self.assertEqual(geohash_adjacent('sr2yk3bsm', 's'), 'sr2yk3bsj')
        self.assertEqual(geohash_adjacent('sr2yk3bsm', 'w'), 'sr2yk3bsk')
        self.assertEqual(geohash_adjacent('sr2yk3bsm', 'e'), 'sr2yk3bsq')

    def test_neighbour(self):
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'nw'), 'sr2yk3bss')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'n'), 'sr2yk3bst')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'ne'), 'sr2yk3bsw')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'w'), 'sr2yk3bsk')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'e'), 'sr2yk3bsq')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'sw'), 'sr2yk3bsh')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 's'), 'sr2yk3bsj')
        self.assertEqual(geohash_neighbour('sr2yk3bsm', 'se'), 'sr2yk3bsn')

    def test_neighbours(self):
        self.assertEqual(geohash_neighbours('sr2yk3bsm'),
                         {'nw': 'sr2yk3bss', 'n': 'sr2yk3bst', 'ne': 'sr2yk3bsw',
                          'w': 'sr2yk3bsk', 'e': 'sr2yk3bsq',
                          'sw': 'sr2yk3bsh', 's': 'sr2yk3bsj', 'se': 'sr2yk3bsn'})

if __name__ == '__main__':
    unittest.main()