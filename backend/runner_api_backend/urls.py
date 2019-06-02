from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from runner_api_backend.views import PointViewSet, \
        RunPathViewSet, RunAreaViewSet, ClusterViewSet

schema_view = get_schema_view(title='Runtastic Data')

router = DefaultRouter()
router.register(r'points', PointViewSet, basename='points')
router.register(r'runpaths', RunPathViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'runareas', RunAreaViewSet)

urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
]
urlpatterns += [
    path('api-auth', include('rest_framework.urls'))
]
