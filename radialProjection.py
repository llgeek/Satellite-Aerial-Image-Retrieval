"""
__author__ = Leon Debnath
__email__ = leon_debnath@hotmail.co.uk

@Description: This module allows for coordinate shifting by arbitrary meter distances and creation of bounding boxes
around decimal degree coordinates. **Note**: these calculations are only approximations, for accurate distance
measurements and projections use a library like GDAL.
"""

from math import pi, cos


def coordinate_shift(latitude: float, longitude: float, lat_shift_meters: float, lon_shift_meters: float):
    """
    Shift a coordinate by some (x, y) meters.

        Arguments:
            latitude {[float]} -- [the starting latitude]
            longitude {[float]} -- [the starting longitude]
            lat_shift_meters {[int]} -- [No. of meters to shift the latitude by (positive = north)]
            lon_shift_meters {[int]} -- [No. of meters to shift the longitude by (positive = east)]

        Returns:
            float, float -- [the new location as a (latitude, longitude) tuple]
    """
    earth_radius = 6378.137

    meter = (1 / ((2 * pi / 360) * earth_radius)) / 1000
    new_latitude = latitude + (lat_shift_meters * meter)
    new_longitude = longitude + (lon_shift_meters * meter) / cos(latitude * (pi / 180))

    return new_latitude, new_longitude


def bounding_box(latitude: float, longitude: float, width_meters: float, height_meters: float):
    """
    Create a bounding box of size width x height meters around the centre point of the coordinates inputted.

        Arguments:
            latitude {[float]} -- [the starting latitude]
            shift_meters {[int]} -- [the number of meters to shift the latitude by]

        Returns: [float, float, float, float] -- [a bounding box with top left and bottom right coordinates lat1,
        lon1, lat2, lon2]
    """
    top_left = coordinate_shift(latitude, longitude, height_meters/2, -width_meters/2)
    bottom_right = coordinate_shift(latitude, longitude, -height_meters/2, width_meters/2)
    return top_left[0], top_left[1], bottom_right[0], bottom_right[1]
