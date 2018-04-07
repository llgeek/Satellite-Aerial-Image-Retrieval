"""
__author__ = Linlin Chen
__email__ = lchen96@hawk.iit.edu

@Description:
This module implements a set of static methods used for Bing maps tile system. 

reference: https://msdn.microsoft.com/en-us/library/bb259689.aspx
"""

import os
from math import cos, sin, pi, log, atan, exp, floor
from itertools import chain
import re


class TileSystem(object):
    
    EARTHRADIUS = 6378137
    MINLAT, MAXLAT = -85.05112878, 85.05112878
    MINLON, MAXLON = -180., 180.
    MAXLEVEL = 23

    @staticmethod
    def clip(val, minval, maxval):
        """Clips a number to be specified minval and maxval values.
        
        Arguments:
            val {[double]} -- [value to be clipped]
            minval {[double]} -- [minimal value bound]
            maxval {[double]} -- [maximal value bound]
        
        Returns:
            [double] -- [clipped value]
        """
        return min(max(val, minval), maxval)

    @staticmethod
    def map_size(level):
        """Determines the map width and height (in pixels) at a specified level
        
        Arguments:
            level {[int]} -- [level of detail, from 1 (lowest detail) to 23 (highest detail)]

        Returns:
            [int] -- [The map width and height in pixels (width == height)]
        """
        return 256 << level

    @staticmethod
    def ground_resolution(lat, level):
        """Determines the ground resolution (in meters per pixel) at a specified latitude and level of detail
        
        Arguments:
            lat {[double]} -- [latitude in degrees at which to measure the ground resolution]
            level {[int]} -- [level of detail, from 1 (lowest detail) to 23 (highest detail)]
        
        Returns:
            [double] -- [The ground resolution, in meters per pixel]
        """

        lat = TileSystem.clip(lat, TileSystem.MINLAT, TileSystem.MAXLAT)
        return cos(lat * pi / 180) * 2 * pi * TileSystem.EARTHRADIUS / TileSystem.map_size(level)


    @staticmethod
    def map_scale (lat, level, screenDpi):
        """Determines the map scale at a specified latitude, level of detail, and screen resolution
        
        Arguments:
            lat {[double]} -- [latitude in degrees at which to measure the ground resolution]
            level {[type]} -- [level of detail, from 1 (lowest detail) to 23 (highest detail)]
            screenDpi {[type]} -- [Resolution of the screen, in dots per inch]
        
        Returns:
            [double] -- [The map scale, expressed as the denominator N of the ratio 1: N]
        """

        return TileSystem.ground_resolution(lat, level) * screenDpi / 0.0254

    @staticmethod
    def latlong_to_pixelXY(lat, long, level):
        """Converts a point from latitude/longitude WGS-84 coordinates (in degrees)
        into pixel XY coordinates a specified level of detail
        
        Arguments:
            lat {[double]} -- [Latitude of the point, in degrees]
            long {[double]} -- [Longitude of the point, in degrees]
            level {[int]} -- [Level of detail, from 1 (lowest detail) to 23 (highest detail)]
        
        Returns:
            [int, int] -- [X coordinates in pixels; Y coordinates in pixels]
        """

        lat = TileSystem.clip(lat, TileSystem.MINLAT, TileSystem.MAXLAT)
        long = TileSystem.clip(long, TileSystem.MINLON,  TileSystem.MAXLON)

        x = (long + 180) / 360
        sinlat = sin(lat * pi / 180)
        y = 0.5 - log((1 + sinlat) / (1 - sinlat)) / (4 * pi)

        mapsize = TileSystem.map_size(level)
        pixelX, pixelY = floor(TileSystem.clip(x * mapsize + 0.5, 0, mapsize - 1)), \
                        floor(TileSystem.clip(y * mapsize + 0.5, 0, mapsize - 1))
        return pixelX, pixelY


    @staticmethod
    def pixelXY_to_latlong(pixelX, pixelY, level):
        """Converts a pixel from pixel XY coordinates at a specified level of detail
        into latitude/longitude WGS-84 coordinates (in degrees)
        
        Arguments:
            pixelX {[int]} -- [X coordinate of the point, in pixels.]
            pixelY {[int]} -- [Y coordinate of the point, in pixels.]
            level {[int]} -- [Level of detail, from 1 (lowest detail) to 23 (highest detail)]
        
        Returns:
            [double, double] -- [Latitude in degrees; Longitude in degrees]
        """

        mapsize = TileSystem.map_size(level)
        x = TileSystem.clip(pixelX, 0, mapsize - 1) / mapsize - 0.5
        y = 0.5 - 360 * TileSystem.clip(pixelY, 0, mapsize - 1) / mapsize

        lat = 90 - 360 * atan(exp(-y * 2 * pi)) / pi 
        long = 360 * x 
        return lat, long


    @staticmethod
    def pixelXY_to_tileXY(pixelX, pixelY):
        """Converts pixel XY coordinates into tile XY coordinates of the tile containing the specified pixel.
        
        Arguments:
            pixelX {[int]} -- [Pixel X coordinate]
            pixelY {[int]} -- [Pixel Y coordinate]
        
        Returns:
            [int, int] -- [Tile X coordinate; Tile Y coordinate]
        """

        return floor(pixelX / 256), floor(pixelY / 256)


    @staticmethod
    def tileXY_to_pixelXY(tileX, tileY):
        """Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel of the specified tile
        
        Arguments:
            tileX {[int]} -- [Tile X coordinate]
            tileY {[int]} -- [Tile Y coordinate]
        
        Returns:
            [int, int] -- [pixel X coordinate; pixel Y coordinate]
        """

        return tileX * 256, tileY * 256


    @staticmethod
    def tileXY_to_quadkey(tileX, tileY, level):
        """Converts tile XY coordinates into a QuadKey at a specified level of detail
        interleaving tileY with tileX
        
        Arguments:
            tileX {[int]} -- [Tile X coordinate]
            tileY {[int]} -- [Tile Y coordinate]
            level {[int]} -- [Level of detail, from 1 (lowest detail) to 23 (highest detail)]
        
        Returns:
            [string] -- [A string containing the QuadKey]
        """

        tileXbits = '{0:0{1}b}'.format(tileX, level)
        tileYbits = '{0:0{1}b}'.format(tileY, level)
        
        quadkeybinary = ''.join(chain(*zip(tileYbits, tileXbits)))
        return ''.join([str(int(num, 2)) for num in re.findall('..?', quadkeybinary)])
        #return ''.join(i for j in zip(tileYbits, tileXbits) for i in j)
        
    @staticmethod
    def quadkey_to_tileXY(quadkey):
        """Converts a QuadKey into tile XY coordinate
        
        Arguments:
            quadkey {[string]} -- [QuadKey of the tile]
        
        Returns:
            [int, int] -- [Tile X coordinate; Tile Y coordinate]
        """
        quadkeybinary = ''.join(['{0:02b}'.format(int(num)) for num in quadkey])
        tileX, tileY = int(quadkeybinary[1::2], 2), int(quadkeybinary[::2], 2)
        return tileX, tileY




