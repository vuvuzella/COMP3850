from celery import shared_task
from celery.contrib import rdb
from .algorithms import findCluster
from .models import Cluster, RunArea, RunPath
from rest_framework.parsers import JSONParser
from .serializers import RunPathSerializer, \
        RunAreaSerializer, ClusterSerializer
import io
from OSMPythonTools.nominatim import Nominatim
from rest_framework import serializers
from django.contrib.auth.models import User

@shared_task
def run_findCluster(data):
    """
    kwargs contains the run_data
    """
    # runpath_serializer = RunPathSerializer(data=data, partial=True)
    osm_endpoint = 'http://nominatim.openstreetmap.org/reverse'
    nm = Nominatim(endpoint=osm_endpoint, waitBetweenQueries=5)
    # serialize into json 
    clusters = [ClusterSerializer(cluster).data for cluster in Cluster.objects.all()]
    run_areas = [ RunAreaSerializer(area).data for area in RunArea.objects.all() ]
    same_cluster = findCluster(data, clusters, dist_thresh=50)

    if same_cluster is None:
        # Reverse Geocode longitude and latitude
        # add a new cluster to the database
        lat = data['latitude']
        lon = data['longitude']
        rev_geocode = nm.query('', params={
            'lat': lat,
            'lon': lon
            })
        json = rev_geocode.toJSON()
        address = json['address']
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
        area_name = area + ' ' + suburb

        # find if area_name exists
        match_run_area = findCluster(data, run_areas)

        # Add an area 
        if match_run_area is None:
            runarea_serializer = RunAreaSerializer(data={
                'area_name': area_name,
                'latitude': lat,
                'longitude': lon
                })
            if runarea_serializer.is_valid():
                runarea_serializer.save()
            match_run_area = runarea_serializer.data

        # Add the cluster
        cluster_serializer = ClusterSerializer(data={
            'area': match_run_area['id'],
            'latitude': lat,
            'longitude': lon
            })
        if cluster_serializer.is_valid():
            # rdb.set_trace() # debug
            cluster_serializer.save()

        same_cluster = cluster_serializer.data

    # # set the clusterId on 
    # # save the data using the RunPathSerializer
    runpath_data = RunPath.objects.filter(id=data['id'])[0]
    runpath_serializer = RunPathSerializer(runpath_data,
            data={'cluster': same_cluster['id']}, partial=True)
    # rdb.set_trace() # debug
    if runpath_serializer.is_valid():
        runpath_serializer.save()

    # return 'Clustered as %s' %
    # rdb.set_trace() # debug
    return
