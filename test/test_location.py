# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 20:53:00 2017

@author: Alessandro Adamo
"""
import unittest
from gea.location import *

class TestLocation(unittest.TestCase):

    def test_radius_spheroid(self):
        self.assertEqual(radius_spheroid(0.0), 6378137.0)
        self.assertEqual(radius_spheroid(90.0), 6356752.3)
        self.assertEqual(radius_spheroid(45.0), 6367444.65)


if __name__ == '__main__':
    unittest.main()