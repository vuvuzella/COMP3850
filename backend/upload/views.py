from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.core.files.uploadedfile import TemporaryUploadedFile

from commons.algorithms import getCentroid, getSemiToLatlon
from fitparse import FitFile
from requests.auth import HTTPBasicAuth
from celery.result import AsyncResult

import zlib
import json
import xml.etree.ElementTree as ET
import math
import os

from .tasks import upload_run_data

def upload(request):

    if (request.method == 'GET'):
        if 'result' in request.GET.keys():
            result = request.GET['result']
        else:
            result = None

        template = loader.get_template('upload/upload.html')
        return HttpResponse(template.render({
            'result': result
            }, request))

    elif (request.method == 'POST'):
        # handle post requests
        # read the file
        # create server endpoint 
        root_host = os.environ.get('APP_DOMAIN')
        request_port = request.META['SERVER_PORT']
        if root_host is None:
            root_host = 'http://localhost:' + request_port
        runpaths_uri = '/'.join([root_host, 'runpaths/'])
        points_uri = '/'.join([root_host, 'points/'])
        user = os.environ.get('UPLOAD_USER')
        passwd = os.environ.get('UPLOAD_PASS')

        endpoints = {
            'runpaths': runpaths_uri,
            'points': points_uri
        }

        if user is None or passwd is None:
            # local
            user = 'admin'
            passwd = 'admin'
        else:
            # use heroku config variables
            pass

        data_type = request.POST['data_type']

        # data structure:
        # [({run_paths} , [{points}]), ...] 
        upload_data = None
        if data_type == 'runtastic':
            activities = request.FILES.getlist('runtastic-activities')
            points = request.FILES.getlist('runtastic-points')
            upload_data = _processRuntasticData(activities, points)
        else:
            points = request.FILES.getlist('strava-points')
            activities = request.FILES.getlist('strava-activities')
            # get all files in activities
            activities = str(activities[0].read())
            activities = activities.split('\\n')[1:-1]
            upload_data = _processStravaData(activities, points)

        if len(upload_data) == 0:
            return HttpResponse(loader
                    .get_template('upload/upload.html')
                    .render({
                        'result': 'failed'
                        }, request))
        else:
            print('data to send: ', len(upload_data))
            task_ids = [upload_run_data.delay(endpoints, datum, user, passwd)
                    for datum in upload_data]
            # load in progress
            template = loader.get_template('upload/in_progress.html')
            return HttpResponse(template.render({
                'job_tasks': task_ids,
                'poll': True,
                'endpoint': root_host + '/upload/in_progress/'
                }, request))

    else:
        return HttpResponse('Method %s not allowed' % (request.method,))

def _getLatLong(runPointsFile, extension):
    """
    Returns a list of lat long tuples
    """
    latlong = None
    if extension == 'gpx':
        latlong = _getPointsFromGpx(runPointsFile)
    else:
        if extension == 'gz':
            dataFile = zlib.decompress(runPointsFile, zlib.MAX_WBITS|16)
        else:
            dataFile = runPointsFile
        fitFile = FitFile(dataFile)
        latlong = _getPointsFromFit(fitFile)
    return latlong

def _getPointsFromGpx(gpxFile):
    """
    Computes for the latitude and the longitude points given a gpx
    file.
    Returns a list of dictionary with keys latitude and longitude
    """
    root = ET.fromstring(gpxFile)
    timedate = root.getchildren()[0]
    segments = root.getchildren()[1][2]
    latlon = []
    for seg in segments:
        lat = float(seg.attrib['lat'])
        lon = float(seg.attrib['lon'])
        latlon.append({
            'latitude': lat,
            'longitude': lon
        })
    return latlon

def _getPointsFromFit(fitFile):
    """
    Returns a list of lat lon dicts in degrees
    """
    latlon = []
    messages = list(fitFile.get_messages(name='record'))
    for message in messages:
        columns = message.get_values()
        if ('position_lat' in columns.keys()) and ('position_long' in columns.keys()):
            lat, lon = getSemiToLatlon(columns['position_lat'],
                    columns['position_long'])
            latlon.append({
                'latitude': lat,
                'longitude': lon
            })
    return latlon

def _processRuntasticData(activities, points):
    """
    Do runtastic processing
    session and gps json data to process
    Both session and gps data should exist to be added to the
    database
    """
    upload_data = []

    for activity in activities:
        # get the activity's lat, lon centroid
        # distance, duration, elevation_gain, elevation_loss
        activity_filename = activity.name
        activity_data = activity.read().decode('utf-8')
        activity_json = json.loads(activity_data)

        activity_keys = activity_json.keys()
        if 'latitude' in activity_keys:
            lat = float(activity_json['latitude'])
        if 'longitude' in activity_keys:
            lon = float(activity_json['longitude'])
        if 'distance' in activity_keys:
            distance = int(activity_json['distance'])
        if 'duration' in activity_keys:
            duration = int(activity_json['duration'])
        if 'elevation_gain' in activity_keys:
            elevation_gain = int(activity_json['elevation_gain'])
        if 'elevation_loss' in activity_keys:
            elevation_loss = int(activity_json['elevation_loss'])

        for point in points:
            point_filename = point.name

            if point_filename == activity_filename:
                # process the point
                point_data = point.read().decode('utf-8')
                point_json = json.loads(point_data)

                # create the run_path_payload
                run_path_payload = None
                run_path_payload = {
                    'latitude': lat,
                    'longitude': lon,
                    'distance': distance,
                    'duration': duration,
                    'cluster': '',
                    'elevation_gain': elevation_gain,
                    'elevation_loss': elevation_loss
                }

                # create the run_poins_payload
                # POST to runner_app api
                run_points_payload = []
                for gps_data in point_json:
                    run_points_payload.append({
                        # 'run_path': run_id,
                        'latitude': float(gps_data['latitude']),
                        'longitude': float(gps_data['longitude']),
                        'elevation_loss': int(gps_data['elevation_loss']),
                        'elevation_gain': int(gps_data['elevation_gain']),
                        'altitude': int(gps_data['altitude']),
                        'distance': int(gps_data['distance'])
                    })

                upload_data.append((run_path_payload, run_points_payload,))
                break
            else:
                # continue searching 
                pass
        # Search for the corresponding GPS data points 
        # break
    return upload_data

def _processStravaData(activities, points):
    """
    Do Strava processing
    """
    upload_data = []
    for activity in activities:
        # load  the corresponding fit, fit.gz or gpx file
        activity_split = activity.split(',')
        point_filename = activity_split[-1].split('/')[-1]
        activity_type = activity_split[3] # gets the 4th column
        extension = point_filename.split('.')[-1]

        if activity_type == 'Run':
            # search for the corresponding
            for point_data in points:
                # Search for corresponding point data
                if point_data.name == point_filename:

                    duration = float(activity_split[5])
                    distance = math.ceil(float(activity_split[6]))
                    latlong = _getLatLong(point_data.read(), extension)
                    if len(latlong) == 0:
                        print('skipping ', point_data.name, 'no latlong retrieved')
                        break;
                    centroid = getCentroid(latlong)

                    # Create the run path payload
                    run_path_payload = {
                        'latitude': centroid[0],
                        'longitude': centroid[1],
                        'distance': distance,
                        'duration': duration,
                        'cluster': '',
                    }

                    # put the run path id on each lat lon poin
                    # for point in latlong:
                    #     point['run_path'] = run_id
                    upload_data.append((run_path_payload, latlong,))
                    break
                else:
                    # Skip this activity because GPS points data could
                    # not be found.
                    pass
        else:
            # Not a run, skip the the activity
            pass
    return upload_data

def in_progress(request):
    if request.method == 'GET':
        if 'job_ids' in request.GET.keys():
            job_ids = request.GET['job_ids'].split('&')[0]
            job_ids = job_ids.split(',')
            results = [ AsyncResult(job_id).state == 'SUCCESS' for job_id in job_ids ]
            print('Job id: ', job_ids[0], 'status: ', AsyncResult(job_ids[0]).state)
            return JsonResponse({'results': results}, safe=False)
        else:
            return HttpResponse('Method %s not allowed' % (request.method,))
    else:
        return HttpResponse('Method %s not allowed' % (request.method,))
