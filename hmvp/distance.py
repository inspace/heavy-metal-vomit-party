import numpy as np
from math import radians, sin, cos, asin, sqrt, pi, atan2

def dist_vector(needle, haystack):
    #values are associated hackstack data. For instance haystack is a list of Google site locations
    #values are the IPs associated with those locations by index.
    lats = [x[0] for x in haystack]
    lons = [x[1] for x in haystack]

    dlat = np.radians(lats) - radians(needle[0])
    dlon = np.radians(lons) - radians(needle[1])
    a = np.square(np.sin(dlat/2.0)) + cos(radians(needle[0])) * np.cos(np.radians(lats)) * np.square(np.sin(dlon/2.0))
    great_circle_distance = 2 * np.arcsin(np.minimum(np.sqrt(a), np.repeat(1, len(a))))
    d = 6367 * great_circle_distance  #vector of distances
    return d

def closest(needle, haystack, values):
    d = dist_vector(needle, haystack)
    i = np.argmin(d)          #index of minimum distance
    return (d[i], values[i])  #return tuple with distance and matching ip

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def degree_dist(lat):
    """
    length of 1 degree in km at the given latitude
    """
    return (pi/180)*6378*cos(radians(lat))

def valid(lat, lon):
    return lat <= 90 and lat >= -90 and lon <= 180 and lon >= -180

def within(needle, haystack, values, dist):
    d = dist_vector(needle, haystack)
    i = np.where(d < dist) #array of indexes of distances less than dist
    dists = d[i]             #numpy-specific. extract all indexes in i from d
    elements = [values[x] for x in i[0]]
    return zip(dists, elements)

def dist_filter(points, max_dist):
    """
    Discard points that within max_dist of another point.
    TODO: This can be much, much better
    """
    discard_set = set()
    point_set = set(points)

    for p1 in point_set:
        for p2 in point_set:
            if p1 not in discard_set and p2 not in discard_set and p1 != p2:
                dist = haversine(p1[0], p1[1], p2[0], p2[1])
                if dist <= max_dist:
                    discard_set.add(p2)

    keep = point_set.difference(discard_set)
    return keep
