from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sample.views import salesman_list, city_list, route_list, SalesmanViewSet, CityViewSet, RouteViewSet

router = DefaultRouter()
router.register(r'salesmen', SalesmanViewSet)
router.register(r'cities', CityViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('salesmen/', salesman_list, name='salesman_list'),
    path('cities/', city_list, name='city_list'),
    path('routee/', route_list, name='route_list'),
    path('api/', include(router.urls)),
]