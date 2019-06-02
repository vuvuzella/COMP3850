from rest_framework import serializers
from runner_api_backend.models import Point, RunPath, RunArea, Cluster
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    """
    ModelSerializer for auth.Users model
    """
    # run_path is a reverse relationship from User to run_path 
    run_paths = serializers.PrimaryKeyRelatedField(many=True,
            queryset=RunPath.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'run_paths')

class RunPathSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for RunPath model
    """
    cluster = serializers.PrimaryKeyRelatedField(
            queryset=Cluster.objects.all(), allow_null=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RunPath
        fields = ('id','user', 'longitude', 'latitude', 'distance', 'id_name',
                'duration', 'cluster', 'elevation_gain', 'elevation_loss')

class PointSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for Point model
    """
    run_path = serializers.PrimaryKeyRelatedField(
            queryset=RunPath.objects.all())

    class Meta:
        model = Point
        fields = ('id', 'run_path', 'longitude', 'latitude', 'altitude',
                'distance', 'elevation_gain', 'elevation_loss')

class RunAreaSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for RunArea
    """
    class Meta:
        model = RunArea
        fields = ('id', 'area_name', 'longitude', 'latitude')

class ClusterSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for Cluster model
    """
    area = serializers.PrimaryKeyRelatedField(many=False,
            queryset=RunArea.objects.all())
    class Meta:
        model = Cluster
        fields = ('id', 'area', 'longitude', 'latitude')


