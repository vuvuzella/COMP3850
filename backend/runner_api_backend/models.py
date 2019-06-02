from django.db import models

# Create your models here.
class RunArea(models.Model):
    """
    An area where a number of clusters belong to
    """
    area_name = models.TextField()
    longitude = models.DecimalField(max_digits=20, decimal_places=16)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)
    class Meta:
        ordering = ('id',)

class Cluster(models.Model):
    """
    the cluster classification a RunPath will belong to
    """
    area = models.ForeignKey(RunArea, related_name='clusters',
            on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=20, decimal_places=16)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)

    class Meta:
        ordering = ('id',)

class RunPath(models.Model):
    """
    The activity that contains the points that constitude the activity.
    Also contains generic activity information
    """
    # Essential fields
    user = models.ForeignKey('auth.User', related_name='run_paths',
            on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, related_name='run_paths',
            on_delete=models.SET_NULL, null=True)
    distance = models.BigIntegerField()
    duration = models.BigIntegerField(null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=16)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)

    # Strava specific 
    # elevation_max
    # elevation_min

    # Runtastic Specific 
    elevation_gain = models.IntegerField(null=True)
    elevation_loss = models.IntegerField(null=True)
    id_name = models.CharField(max_length=100, null=True)
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()
    # start_time_timezone_offset = models.BigIntegerField()
    # end_time_timezone_offset = models.BigIntegerField()
    # average_speed = models.DecimalField(max_digits=20, decimal_places=16)
    # calories = models.IntegerField()
    # max_speed = models.DecimalField(max_digits=20, decimal_places=16)
    # duration_per_km = models.IntegerField()
    # temperature = models.IntegerField()
    # manual = models.BooleanField()
    # edited = models.BooleanField()
    # completed = models.BooleanField()
    # live_tracking_active = models.BooleanField()
    # live_tracking_enabled = models.BooleanField()
    # cheering_enabled = models.BooleanField()
    # indoor = models.BooleanField()
    # id in the Runtastic json data
    # might not be needed, depending on how the data is represented in the
    # schema
    # weather_condition_id = models.IntegerField()
    # sport_type_id = models.IntegerField()

    # The points that constitute the run
    # points = models.ForeignKey(Point, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

class Point(models.Model):
    """
    A point that correspond to a single longitude and latitude mark
    of a run
    """
    run_path = models.ForeignKey(RunPath, on_delete=models.CASCADE,
            related_name='points')
    longitude = models.DecimalField(max_digits=20, decimal_places=16)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)
    altitude = models.DecimalField(max_digits=20, decimal_places=16, null=True)
    distance = models.BigIntegerField(null=True)
    elevation_gain = models.IntegerField(null=True)
    elevation_loss = models.IntegerField(null=True)
    # timestamp = models.DateTimeField()
    # speed = models.DecimalField(max_digits=20, decimal_places=16)
    # duration = models.BigIntegerField()
    # version = models.CharField(max_length=50)
    # accuracy_v = models.IntegerField()
    # accuracy_h = models.IntegerField()

    class Meta:
        ordering = ('id',)
