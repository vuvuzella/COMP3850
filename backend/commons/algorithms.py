import json
import os
import math
import re

from geographiclib.geodesic import Geodesic
from geographiclib.constants import Constants

def deg2rad(deg):
    """
    Convert degrees to radians
    """
    return deg * (math.pi / 180.0)

def getEucledianDistance(x2, y2, x1, y1):
    """
    Not accurate compared to the distance calculated by runtastic apps
    """
    x_diff = math.fabs(deg2rad(x2) - deg2rad(x1))
    y_diff = math.fabs(deg2rad(y2) - deg2rad(y1))
    return math.sqrt((x_diff ** 2) + (y_diff ** 2))

def getHaversineDistance(x2, y2, x1, y1):
    """
    x - longitude
    y - latitude
    """
    pt2 = (deg2rad(x2), deg2rad(y2))
    pt1 = (deg2rad(x1), deg2rad(y1))
    delta_y = deg2rad(y2 - y1)
    delta_x = deg2rad(x2 - x1)

    sin_square_diff_y = math.sin(delta_y/2.0) ** 2

    cos_y2 = math.cos(pt2[1])
    cos_y1 = math.cos(pt1[1])

    sin_square_diff_x = math.sin(delta_x/2.0) ** 2

    half_chord_length = sin_square_diff_x + (cos_y2 * cos_y1 *
            sin_square_diff_x)

    angular_dist_rad = 2 * math.atan2(math.sqrt(half_chord_length),
            math.sqrt(1 - half_chord_length))

    earth_radius = Constants.WGS84_a   # Earth's radius in meters

    return math.floor(earth_radius * angular_dist_rad)

def getGeodesicDistance(x2, y2, x1, y1):
    """
    Uses Inverse function of geographiclib to calculate the geodesic distance
    between 2 long-lat points using WGS84 standards
    Return value is in meters
    x - longitude
    y - latitude
    """
    pt2 = (deg2rad(x2), deg2rad(y2))
    pt1 = (deg2rad(x1), deg2rad(y1))
    return Geodesic.WGS84.Inverse(y1, x1, y2, x2,
            outmask=Geodesic.DISTANCE)['s12']

def clusterByCentroids(run_gps_data, f=getGeodesicDistance, diff_thresh=50):
    """
    Creates a clustered dictionary of all running gps data
    """
    cluster = {}
    similarity_found = False;

    for run_data in run_gps_data:
        # compare in each data inside the dictionary
        for key in cluster.keys():
            run_dict = cluster.get(key)
            # Use f function to calculate distance between two points
            dist = f(run_dict['longitude'], run_dict['latitude'], run_data['longitude'],
                    run_data['latitude'])
            if dist < diff_thresh:
                # similar!
                run_dict['variations'].append(run_data)
                similarity_found = True
                break
            else:
                # different
                pass

        # No similar tracks found, add as new track
        if not similarity_found:
            run_data['variations'] = []
            cluster[run_data['id']] = run_data
        else:
            similarity_found = False
    return cluster

def getTotalDistance(run_points_data, f):
    """
    Computes for the distace using f as the function that calculates the
    distandistance between points in run_points_data
    """
    total_distance = 0
    for idx, point in enumerate(run_points_data):
        if idx > 0:
            pt2 = run_points_data[idx]
            pt1 = run_points_data[idx - 1]
            dist_pts = f(pt2['longitude'], pt2['latitude'],pt1['longitude'], pt1['latitude'])
            total_distance += dist_pts
    return total_distance

def findCluster(run_data, cluster_data, dist_thresh=50):
    """
    Searches for a cluster from the given set of clusters
    returns a cluster data or None if none is found
    """

    # TODO: change this to dot reference, instead of string reference?
    run_lat = float(run_data['latitude'])
    run_lon = float(run_data['longitude'])

    for cluster in cluster_data:
        cluster_lat = float(cluster['latitude'])
        cluster_lon = float(cluster['longitude'])

        geoDistance = getGeodesicDistance(cluster_lon, cluster_lat, run_lon, run_lat)

        if geoDistance < dist_thresh:
            return cluster
    # nothing found, return none
    return None

def getCentroid(run_points, semicircle=False):
    """
    Given a list of lat, long points, compute for the centroid
    """
    total_lat = 0
    total_lon = 0
    for point in run_points:
        if semicircle:
            # convert to degrees
            semi_lat = point['latitude']
            semi_lon = point['longitude']
            total_lat += semi_lat * (180 / (2**31) )
            total_lon += semi_lon * (180 / (2**31) )
        else:
            total_lat += point['latitude']
            total_lon += point['longitude']

    cen_lat = total_lat / len(run_points)
    cen_lon = total_lon / len(run_points)
    return (cen_lat, cen_lon)

# if __name__ == '__main__':
#     runtastic_dir = '../data/runtastic/Sport-sessions'
#     # run_filename = 'fffc980a-f785-4e8a-9aa7-55396ad841ba.json'
#     run_filename = '9658ac71-22e0-4a50-bab6-9ec9dcf0fe65.json'
# 
#     run_file = open('/'.join([runtastic_dir, run_filename]))
#     run_points = open('/'.join([runtastic_dir, 'GPS-data', run_filename]))
# 
#     run_data = json.load(run_file)
#     run_points_data = json.load(run_points)
# 
#     print('Centroid from Run file: (%f, %f)' % (run_data['latitude'],
#         run_data['longitude']))
# 
#     lat_p, lon_p = getCentroid(run_points_data)
# 
#     print('Centroid from function: (%f, %f)' % (lat_p, lon_p))
# 
#     run_file.close()
#     run_points.close()
# 
# 
