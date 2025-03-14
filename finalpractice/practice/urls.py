from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, CityViewSet, SalesmanViewSet, solve

router = DefaultRouter()
router.register(r'salesmen', SalesmanViewSet)
router.register(r'cities', CityViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('solve/<uuid:route_id>/', solve, name='solve'),
]
