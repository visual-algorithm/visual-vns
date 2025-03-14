from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sample.views import salesman_list, city_list, route_list, api_solve, api_get_routes, api_delete_route, api_delete_city, api_set_route, api_get_cities, api_get_salesmen, api_data, api_delete_route, api_update_route, SalesmanViewSet, CityViewSet, RouteViewSet

router = DefaultRouter()
router.register(r'salesmen', SalesmanViewSet)
router.register(r'cities', CityViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('salesmen/', salesman_list, name='salesman_list'),
    path('cities/', city_list, name='city_list'),
    path('routes/', route_list, name='route_list'),
    path('api/', include(router.urls)),
    path('api/api_routes/', api_data, name='api_data'),
    path('api/api_solve/', api_solve, name='api_solve'),
    path('api/api_get_routes/', api_get_routes, name='api_get_routes'),
    path('api/api_set_route/', api_set_route, name='api_set_route'),
    path('api/api_delete_route/<int:route_id>/', api_delete_route, name='api_delete_route'),
    path('api/api_delete_city/<int:city_id>/', api_delete_city, name='api_delete_city'),
    path('api/api_get_cities/', api_get_cities, name='api_get_cities'),
    path('api/api_get_salesmen/', api_get_salesmen, name='api_get_salesmen'),
    path('api/api_routes/<int:route_id>/', api_delete_route, name='api_delete_route'),
    path('api/api_routes_edit/<int:route_id>/', api_update_route, name='api_update_route'),
]