# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:48:59 2017

@author: Alessandro Adamo
"""
from math import *


__WGS84 = dict(A=6378137.0, # equatorial radius
               C=6356752.3, # polar radius
               R=(2.0 * 6378137.0 + 6356752.3) / 3.0, # mean radius
               F=(6378137.0 - 6356752.3) / 6378137.0) # flatness


def radius_spheroid(lat: float):
    """
    Radius of spheroid

    :param lat: latitude
    :return: radius of spheroid
    """

    if not -90.0 <= lat <= +90.0:
        raise ValueError('Invalid location latitude')

    return __WGS84['A'] * (1.0 - __WGS84['F'] * sin(radians(lat)) ** 2.0)


def haversine(loc1: dict, loc2: dict):
    """
    Haversine distance

    :param loc1: location point
    :param loc2: location point
    :return: Haversine distance
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    lat1 = radians(loc1['lat'])
    lon1 = radians(loc1['lon'])
    lat2 = radians(loc2['lat'])
    lon2 = radians(loc2['lon'])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = sin(delta_lat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2.0) ** 2
    c = 2.0 * asin(sqrt(a))

    return __WGS84['R'] * c


def haversine_approximation(loc1: dict, loc2: dict):
    """
    Haversine distance approximated by Euclidean distance

    :param loc1: location point
    :param loc2: location point
    :return: Haversine distance
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    lat1 = radians(loc1['lat'])
    lon1 = radians(loc1['lon'])
    lat2 = radians(loc2['lat'])
    lon2 = radians(loc2['lon'])

    x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1

    return __WGS84['R'] * sqrt(x*x + y*y)


def bearing(loc1: dict, loc2: dict):
    """
    Calculate the bearing between this location and the location passed as argument.

    :param loc1: location point
    :param loc2: location point
    :return: bearing
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    lat1 = radians(loc1['lat'])
    lon1 = radians(loc1['lon'])
    lat2 = radians(loc2['lat'])
    lon2 = radians(loc2['lon'])

    delta_lon = lon2 - lon1
    clat2 = cos(lat2)
    y = sin(delta_lon) * clat2
    x = cos(lat1) * sin(lat2) - \
        sin(lat1) * clat2 * cos(delta_lon)

    brng = degrees(atan2(y, x))
    if brng < 0.0:
        brng = 360.0 + brng

    return brng


def destination(loc: dict, dist: float, bearing: float):
    """
    Given a start point and a distance d along a constant bearing, this will calculate the destination point.

    :param loc: location point
    :param dist: distance expressed in meters
    :param bearing: bearing expressed in degrees
    :return: destination point
    """
    if 'lat' not in loc or 'lon' not in loc:
        raise TypeError('Invalid location')

    if (not isinstance(loc['lat'], float)) or (not isinstance(loc['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not 0.0 <= bearing <= 360.0:
        raise ValueError('Invalid location longitude')

    lat1 = radians(loc['lat'])
    lon1 = radians(loc['lon'])
    brng = radians(bearing)

    dr = dist / __WGS84['R']
    lat2 = asin(sin(lat1) * cos(dr) +
                cos(lat1) * sin(dr) * cos(brng))
    y = sin(brng) * sin(dr) * cos(lat1)
    x = cos(dr) - sin(lat1) * sin(lat2)
    lon2 = lon1 + atan2(y, x)

    return {'lat': degrees(lat2), 'lon': degrees(lon2)}


def latlon_to_cartesian(loc: dict):
    """
    Convert latitude/longitude coordinates to 3D Cartesian coordinates.

    :param loc: location point
    :return: 3D Cartesian coordinates
    """
    if 'lat' not in loc or 'lon' not in loc:
        raise TypeError('Invalid location')

    if (not isinstance(loc['lat'], float)) or (not isinstance(loc['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    lat1 = radians(loc['lat'])
    lon1 = radians(loc['lon'])

    slat = sin(lat1)
    clat = cos(lat1)
    slong = sin(lon1)
    clong = cos(lon1)

    if 'alt' in loc:
        if not isinstance(loc['alt'], float):
            raise TypeError('Invalid location altitude')

        x = (__WGS84['R'] + loc['alt']) * clat * clong
        y = (__WGS84['R'] + loc['alt']) * clat * slong
        z = (__WGS84['R'] + loc['alt']) * slat
    else:
        x = __WGS84['R'] * clat * clong
        y = __WGS84['R'] * clat * slong
        z = __WGS84['R'] * slat

    return {'x': x, 'y': y, 'z': z}


def cartesian_to_latlon(car: dict):
    """
    Convert 3D Cartesian coordinates to latitude/longitude coordinates.

    :param: 3D Cartesian coordinates
    :return: location point
    """
    if 'x' not in car or 'y' not in car or 'z' not in car:
        raise TypeError('Invalid cartesian')

    r = sqrt(car['x'] ** 2.0 + car['y'] ** 2.0 + car['z'] ** 2.0)

    alt = r - __WGS84['R']
    lon = atan2(car['y'], car['x']) * 360.0 / (2.0 * pi)
    lat = asin(car['z'] / r) * 360.0 / (2.0 * pi)

    return {'lat': lat, 'lon': lon, 'alt': alt}


def midpoint(loc1: dict, loc2: dict):
    """
    Calculate the half-way point along a great circle path between the two points.

    :param loc1: location point
    :param loc2: location point
    :return: half-way point
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    c1 = latlon_to_cartesian(loc1)
    c2 = latlon_to_cartesian(loc2)

    loc = cartesian_to_latlon({'x': 0.5 * (c1['x'] + c2['x']),
                               'y': 0.5 * (c1['y'] + c2['y']),
                               'z': 0.5 * (c1['z'] + c2['z'])})

    if 'alt' in loc1:
        if not isinstance(loc1['alt'], float):
            raise TypeError('Invalid altitude')
        alt1 = loc1['alt']
    else:
        alt1 = 0.0

    if 'alt' in loc2:
        if not isinstance(loc2['alt'], float):
            raise TypeError('Invalid altitude')
        alt2 = loc2['alt']
    else:
        alt2 = 0.0

    loc['alt'] = 0.5 * (alt1 + alt2)

    return loc


def angle_between(loc1: dict, loc2: dict):
    """
    Returns the angle expressed in radiant between this location and the location passed as argument.
    This is the same as the distance on the unit sphere.

    :param loc1: location point
    :param loc2: location point
    :return: the angle between this point and location point passed as argument
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    c1 = latlon_to_cartesian(loc1)
    c2 = latlon_to_cartesian(loc2)

    return degrees((c1['x'] * c2['x'] + c1['y'] * c2['y'] + c1['z'] * c2['z']) / (__WGS84['R'] ** 2.0))


def interpolate_location(loc1: dict, loc2: dict, fraction: float):
    """
    Returns the location which lies the given fraction of the way between the origin location and the
    destination location.

    :param loc1: location point
    :param loc2: location point
    :param fraction: the fraction of the distance between the two locations
    :return: interpolated location
    """
    if 'lat' not in loc1 or 'lon' not in loc1:
        raise TypeError('Invalid location')

    if 'lat' not in loc2 or 'lon' not in loc2:
        raise TypeError('Invalid location')

    if (not isinstance(loc1['lat'], float)) or (not isinstance(loc1['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc2['lat'], float)) or (not isinstance(loc2['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= loc1['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc1['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc2['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc2['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not 0.0 <= fraction <= 1.0:
        raise ValueError('Invalid fraction')

    lat1 = radians(loc1['lat'])
    lon1 = radians(loc1['lon'])
    lat2 = radians(loc2['lat'])
    lon2 = radians(loc2['lon'])

    cos_lat1 = cos(lat1)
    cos_lat2 = cos(lat2)

    angle = radians(angle_between(loc1, loc2))
    sin_angle = sin(angle)
    a = sin((1.0 - fraction) * angle) / sin_angle
    b = sin(fraction * angle) / sin_angle

    x = a * cos_lat1 * cos(lon1) + b * cos_lat2 * cos(lon2)
    y = a * cos_lat1 * sin(lon1) + b * cos_lat2 * sin(lon2)
    z = a * sin(lat1) + b * sin(lat2)

    loc = cartesian_to_latlon({'x': x, 'y': y, 'z': z})

    if 'alt' in loc1:
        if not isinstance(loc1['alt'], float):
            raise TypeError('Invalid altitude')
        alt1 = loc1['alt']
    else:
        alt1 = 0.0

    if 'alt' in loc2:
        if not isinstance(loc2['alt'], float):
            raise TypeError('Invalid altitude')
        alt2 = loc2['alt']
    else:
        alt2 = 0.0

    loc['alt'] = fraction * (alt1 + alt2)

    return loc


def cross_track_distance(orig: dict, dest: dict, loc: dict):
    """
    Cross Track Distance compute the distance from the point loc and the segment passing throw orig point and
    the dest point.

    :param orig: origin point
    :param dest: destination point
    :param loc: third point
    :return: cross track distance
    """
    if 'lat' not in orig or 'lon' not in orig:
        raise TypeError('Invalid location')

    if 'lat' not in dest or 'lon' not in dest:
        raise TypeError('Invalid location')

    if 'lat' not in loc or 'lon' not in loc:
        raise TypeError('Invalid location')

    if (not isinstance(orig['lat'], float)) or (not isinstance(orig['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(dest['lat'], float)) or (not isinstance(dest['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc['lat'], float)) or (not isinstance(loc['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= orig['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= orig['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= dest['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= dest['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    return asin(sin(haversine(orig, loc) / __WGS84['R']) *
                sin(radians(bearing(orig, dest)) - radians(bearing(orig, loc)))) * __WGS84['R']


def along_track_distance(orig: dict, dest: dict, loc: dict):
    """
    Along Track Distances is the distance from the start point to the closest point on the path to a third
    point loc, following a great circle path defined by this point and dest.

    :param orig: origin point
    :param dest: destination point
    :param loc: third point
    :return: cross track distance
    """
    if 'lat' not in orig or 'lon' not in orig:
        raise TypeError('Invalid location')

    if 'lat' not in dest or 'lon' not in dest:
        raise TypeError('Invalid location')

    if 'lat' not in loc or 'lon' not in loc:
        raise TypeError('Invalid location')

    if (not isinstance(orig['lat'], float)) or (not isinstance(orig['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(dest['lat'], float)) or (not isinstance(dest['lon'], float)):
        raise TypeError('Invalid location')

    if (not isinstance(loc['lat'], float)) or (not isinstance(loc['lon'], float)):
        raise TypeError('Invalid location')

    if not -90.0 <= orig['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= orig['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= dest['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= dest['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    if not -90.0 <= loc['lat'] <= +90.0:
        raise ValueError('Invalid location latitude')

    if not -180.0 <= loc['lon'] <= +180.0:
        raise ValueError('Invalid location longitude')

    d_ol = haversine(orig, loc) / __WGS84['R']
    dxt = asin(sin(d_ol) *
               sin(radians(bearing(orig, dest)) - radians(bearing(orig, loc)))) * __WGS84['R']

    cross_track_distance(orig, dest, loc)
    return acos(cos(d_ol) / cos(dxt / __WGS84['R'])) * __WGS84['R']


if __name__ == "__main__":

    # Colosseum - Rome
    loc1 = {'lat': 41.890251, 'lon': 12.492373, 'alt': 137.0}
    # Duomo - Milan
    loc2 = {'lat': 45.464211, 'lon': 9.191383}

    # Pisa
    loc3 = {'lat': 43.7166667, 'lon': 10.3833333}

    print(f'haversine: {haversine(loc1, loc2)}')
    print(f'haversine approximation: {haversine_approximation(loc1, loc2)}')


    a = latlon_to_cartesian(loc1)
    print(f'latlon2cart: {a}')

    a = cartesian_to_latlon(latlon_to_cartesian(loc1))
    print(f'cart2latlon: {a}')

    print(f'bearing: {bearing(loc1, loc2)}')

    print(f'destination: {destination(loc1, dist=10000.0, bearing=45.0)}')

    print(f'midpoint: {midpoint(loc1, loc2)}')

    print(f'interpolate: {interpolate_location(loc1, loc2, 0.3)}')
    print(f'interpolate: {interpolate_location(loc1, loc2, 0.5)}')
    print(f'interpolate: {interpolate_location(loc1, loc2, 0.8)}')

    print(f'angle between: {angle_between(loc1, loc2)}')

    print(f'cross track distance: {cross_track_distance(loc1, loc2, loc3)}')
    print(f'along track distance: {along_track_distance(loc1, loc2, loc3)}')
