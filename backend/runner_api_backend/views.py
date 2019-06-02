from rest_framework import viewsets, status
from rest_framework.response import Response
from runner_api_backend.models import Point, RunPath, RunArea, Cluster
from runner_api_backend.serializers import PointSerializer, \
                                           RunPathSerializer, \
                                           RunAreaSerializer, \
                                           ClusterSerializer
from rest_framework.decorators import action
from .tasks import run_findCluster
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from .permissions import IsUserOrReadOnly

class PointViewSet(viewsets.ModelViewSet):
    # queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly)

    def get_queryset(self):
        queryset = Point.objects.all()
        run_path = self.request.query_params.get('run_path')
        if run_path is not None:
            queryset = queryset.filter(run_path=run_path)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                headers=headers)

class RunPathViewSet(viewsets.ModelViewSet):
    queryset = RunPath.objects.all()
    serializer_class = RunPathSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly)

    # override the creation (POST) of new run paths
    # to actually run the algorithm after saving the run path to 
    # the database
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        run_findCluster.delay(serializer.data)


class RunAreaViewSet(viewsets.ModelViewSet):
    queryset = RunArea.objects.all()
    serializer_class = RunAreaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly)

class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly)
