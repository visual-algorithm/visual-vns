from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, CityViewSet, SalesmanViewSet
from practice import views

router = DefaultRouter()
router.register(r'salesmen', SalesmanViewSet)
router.register(r'cities', CityViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    #ここのurlpath直したい
    path('solve/<uuid:route_id>/', views.solve, name='solve'),
    path('result/<uuid:route_id>/', views.send_result_for_ios, name='result'),
    path('city_new/', views.city_new, name='city_new'),
    path('<uuid:city_id>/city_detail/', views.city_detail, name='city_detail'),
    path('<uuid:city_id>/city_edit/', views.city_edit, name='city_edit'),
    path('route_new/', views.route_new, name='route_new'),
    path('<uuid:route_id>/route_detail/', views.route_detail, name='route_detail'),
    path('<uuid:route_id>/route_edit/', views.route_edit, name='route_edit'),
]
