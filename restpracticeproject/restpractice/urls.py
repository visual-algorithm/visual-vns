from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, SalesmanViewSet, RouteViewSet
from restpractice import views

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'salesmen', SalesmanViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/result/<uuid:route_id>/', views.send_result_for_ios, name='result'),
]
