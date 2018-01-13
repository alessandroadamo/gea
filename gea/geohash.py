# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:48:59 2017

@author: Alessandro Adamo
"""
import math

__base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
__decodemap = {}
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i

__neighbour = {
    'n': ['p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'bc01fg45238967deuvhjyznpkmstqrwx'],
    's': ['14365h7k9dcfesgujnmqp0r2twvyx8zb', '238967debc01fg45kmstqrwxuvhjyznp'],
    'e': ['bc01fg45238967deuvhjyznpkmstqrwx', 'p0r21436x8zb9dcf5h7kjnmqesgutwvy'],
    'w': ['238967debc01fg45kmstqrwxuvhjyznp', '14365h7k9dcfesgujnmqp0r2twvyx8zb']
}

__border = {
    'n': ['prxz', 'bcfguvyz'],
    's': ['028b', '0145hjnp'],
    'e': ['bcfguvyz', 'prxz'],
    'w': ['0145hjnp', '028b']
}


def geohash_encode(loc: dict, precision=10):
    """
    Geohash encode.

    :type loc: dict
    :param loc: location dictionary
    :param precision: length of the geohash string
    :return geohash string
    """
    lat = loc['lat']
    lon = loc['lon']

    if lat is None:
        raise ValueError('Invalid latitude')
    if lon is None:
        raise ValueError('Invalid longitude')
    if lat < -90.0 or lat > 90.0:
        raise ValueError('Invalid latitude')
    if lon < -180.0 or lon > 180.0:
        raise ValueError('Invalid longitude')
    if precision is None:
        raise ValueError('Invalid precision')

    idx = 0
    bit = 0
    even_bit = True
    geohash = ''

    lat_min = -90.0
    lat_max = 90.0
    lon_min = -180.0
    lon_max = 180.0

    while len(geohash) < precision:
        if even_bit:
            # bisect E-W longitude
            lon_mid = (lon_min + lon_max) / 2.0

            if lon >= lon_mid:
                idx = 2 * idx + 1
                lon_min = lon_mid
            else:
                idx = 2 * idx
                lon_max = lon_mid
        else:
            # bisect E-W longitude
            lat_mid = (lat_min + lat_max) / 2.0
            if lat >= lat_mid:
                idx = 2 * idx + 1
                lat_min = lat_mid
            else:
                idx = 2 * idx
                lat_max = lat_mid
        even_bit = not even_bit

        bit += 1
        if bit == 5:
            # next character
            geohash += __base32[idx]
            bit = 0
            idx = 0

    return geohash


def geohash_bounds(geohash: str):
    """
    Returns SW/NE latitude/longitude bounds of specified geohash.

    :param geohash: Cell that bounds are required of.
    :return bounds dictionary
    """
    if geohash is None:
        raise ValueError('Invalid Geohash')
    if len(geohash) == 0:
        raise ValueError('Invalid Geohash invalid')

    geohash = geohash.lower()

    even_bit = True
    lat_min = -90.0
    lat_max = 90.0
    lon_min = -180.0
    lon_max = 180.0

    for i in range(len(geohash)):
        char = geohash[i]
        idx = __decodemap[char]
        if idx == -1:
            raise Exception('Invalid geohash')

        for nn in range(4, -1, -1):
            bit_n = idx >> nn & 1
            if even_bit:
                # longitude
                lon_mid = (lon_min + lon_max) / 2.0
                if bit_n == 1:
                    lon_min = lon_mid
                else:
                    lon_max = lon_mid
            else:
                # latitude
                lat_mid = (lat_min + lat_max) / 2.0
                if bit_n == 1:
                    lat_min = lat_mid
                else:
                    lat_max = lat_mid

            even_bit = not even_bit

    bounds = {
        'sw': {'lat': lat_min, 'lon': lon_min},
        'ne': {'lat': lat_max, 'lon': lon_max}
    }

    return bounds


def geohash_decode(geohash):
    """
    Geohash decode.

    :param geohash: geohash string
    :return location dictionary
    """
    bounds = geohash_bounds(geohash)

    # determine the centre of the cell
    lat_min = bounds['sw']['lat']
    lon_min = bounds['sw']['lon']
    lat_max = bounds['ne']['lat']
    lon_max = bounds['ne']['lon']

    lat = (lat_min + lat_max) / 2.0
    lon = (lon_min + lon_max) / 2.0

    # round to close to centre
    lat = round(lat, int(math.floor(2.0 - math.log(lat_max - lat_min) / math.log(10.0))))
    lon = round(lon, int(math.floor(2.0 - math.log(lon_max - lon_min) / math.log(10.0))))

    return {'lat': lat, 'lon': lon}


def geohash_adjacent(geohash: str, direction: str):
    """
    Determines adjacent cell in given direction.

    :param geohash: geohash string
    :param direction: direction from geohash (n/s/e/w)
    :return geocode of adjacent cell
    """
    if geohash is None:
        raise ValueError('Invalid Geohash')
    if len(geohash) == 0:
        raise ValueError('Invalid Geohash')
    if direction is None:
        raise ValueError('Invalid direction')
    if len(direction) != 1:
        raise ValueError('Invalid direction')

    direction = direction.lower()
    if direction not in 'nsew':
        raise ValueError('Invalid direction')

    geohash = geohash.lower()

    last_ch = geohash[-1]
    parent = geohash[:-1]

    ttype = len(geohash) % 2

    try:
        if __border[direction][ttype].index(last_ch) and parent != '':
            parent = geohash_adjacent(parent, direction)
    except ValueError:
        pass

    return parent + __base32[__neighbour[direction][ttype].index(last_ch)]


def geohash_neighbour(geohash: str, direction: str):
    """
    Determines neighbour cell in given direction.

    :param geohash: geohash string
    :param direction: direction from geohash (nw/n/ne/w/e/sw/s/se)
    :return: geocode of neighbour cell
    """

    if geohash is None:
        raise ValueError('Invalid Geohash')
    if len(geohash) == 0:
        raise ValueError('Invalid Geohash')
    if direction is None:
        raise ValueError('Invalid direction')
    if len(direction) != 1 and len(direction) != 2:
        raise ValueError('Invalid direction')

    direction = direction.lower()
    if direction not in ['nw', 'n', 'ne',
                         'e', 'w',
                         'sw', 's', 'se']:
        raise ValueError('Invalid direction')

    def adj_nw():
        return geohash_adjacent(geohash_adjacent(geohash, 'n'), 'w')

    def adj_n():
        return geohash_adjacent(geohash, 'n')

    def adj_ne():
        return geohash_adjacent(geohash_adjacent(geohash, 'n'), 'e')

    def adj_w():
        return geohash_adjacent(geohash, 'w')

    def adj_e():
        return geohash_adjacent(geohash, 'e')

    def adj_sw():
        return geohash_adjacent(geohash_adjacent(geohash, 's'), 'w')

    def adj_s():
        return geohash_adjacent(geohash, 's')

    def adj_se():
        return geohash_adjacent(geohash_adjacent(geohash, 's'), 'e')

    options = {'nw': adj_nw,
               'n': adj_n,
               'ne': adj_ne,
               'w': adj_w,
               'e': adj_e,
               'sw': adj_sw,
               's': adj_s,
               'se': adj_se}

    return options[direction]()


def geohash_neighbours(geohash: str):
    """
    Returns all 8 adjacent cells to specified geohash

    :param geohash: geohash string
    :return: adjacent cells to specified geohash
    """
    return {
        'nw': geohash_neighbour(geohash, 'nw'),
        'n': geohash_neighbour(geohash, 'n'),
        'ne': geohash_neighbour(geohash, 'ne'),
        'w': geohash_neighbour(geohash, 'w'),
        'e': geohash_neighbour(geohash, 'e'),
        'sw': geohash_neighbour(geohash, 'sw'),
        's': geohash_neighbour(geohash, 's'),
        'se': geohash_neighbour(geohash, 'se')
    }


if __name__ == "__main__":
    # Colosseum - Rome
    location = {'lat': 41.890251, 'lon': 12.492373}

    print(location)
    h = geohash_encode(location, 5)
    b = geohash_bounds(h)
    d = geohash_decode(h)

    print(h)
    print(b)
    print(d)

    n = geohash_adjacent(h, 'n')
    s = geohash_adjacent(h, 's')
    w = geohash_adjacent(h, 'w')
    e = geohash_adjacent(h, 'e')

    print(n)
    print(s)
    print(w)
    print(e)

    print(geohash_neighbours(h))
