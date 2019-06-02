# loadData.py
# load the data that is in json format

import json
import os
import math
import re

from geographiclib.geodesic import Geodesic
from geographiclib.constants import Constants

from OSMPythonTools.nominatim import Nominatim
import urllib.parse

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
    """
    pt2 = (deg2rad(x2), deg2rad(y2))
    pt1 = (deg2rad(x1), deg2rad(y1))
    return Geodesic.WGS84.Inverse(y1, x1, y2, x2,
            outmask=Geodesic.DISTANCE)['s12']

def clusterByCentroids(run_gps_data, f=getGeodesicDistance, diff_thresh=50):
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

def main():
    user = 'data/runtastic'
    sport_sess = 'Sport-sessions'
    gps_dir = 'GPS-data'
    elevation_data = 'Elevation-data'
    cwd = os.getcwd()
    pathToFile = '/'.join([cwd, user, sport_sess])
    all_files = os.listdir(pathToFile)
    osm_endpoint = 'https://nominatim.openstreetmap.org/reverse'
    nm = Nominatim(endpoint=osm_endpoint, waitBetweenQueries=5)
    # nm = Nominatim()

    data = []
    json_file = None
    json_file_regex = re.compile('[a-zA-Z0-9\-]+.json')
    for run_data in all_files:

        if re.match(json_file_regex, run_data):
            json_file = '/'.join([pathToFile, run_data])
            with open(json_file) as f:
                data.append(json.load(f))


    # Examine run data at index 0
    # run_data = data[2]
    # with open('/'.join([os.getcwd(), user, sport_sess, gps_dir,
    #     run_data['id']]) + '.json') as f:
    #     gps_data = json.load(f)

    # print('Run id: ', run_data['id'])
    # print('Number of points: ', len(gps_data))
    # print('Distance from run data: ', run_data['distance'])


    # dist = getTotalDistance(gps_data, getGeodesicDistance)

    # print("Distance computed: ", dist)

    print("Total runs: ", len(data))
    cluster = clusterByCentroids(data)
    print("Clustered runs: ", len(cluster))

    for key, run in cluster.items():
        # run = cluster.get(key)
        print('Latitude: ', run['latitude'])
        print('Longitude: ', run['longitude'])
        print('Variations: ', len(run['variations']))
        result = nm.query('', params={
            'lat': run['latitude'],
            'lon': run['longitude']
            })
        json_data = result.toJSON()
        address = json_data['address']
        if 'county' in address.keys():
            area = address['county']
        elif 'neighbourhood' in address.keys():
            area = address['neighbourhood']
        else:
            area = 'get key'

        if 'suburb' in address.keys():
            suburb = address['suburb']
        elif 'state' in address.keys():
            suburb = address['state']
        else:
            suburb = 'get key'


        # if address['country_code'] == 'au':
        #     area = address['county']
        #     suburb = address['suburb']
        # else:
        #     area = address['neighbourhood']
        #     suburb = address['village']
        print('Area: %s' % (area))
        print('Suburb: %s' % (suburb))
        print('Country: %s' % (address['country']))

if __name__ == '__main__':
    main()
