from django.urls import path

from solutions import views


urlpatterns = [
    path('city_new/', views.city_new, name='city_new'),
    path('<int:city_id>/city_detail/', views.city_detail, name='city_detail'),
    path('<int:city_id>/city_edit/', views.city_edit, name='city_edit'),
    path('route_new/', views.route_new, name='route_new'),
    path('<int:route_id>/route_detail/', views.route_detail, name='route_detail'),
    path('<int:route_id>/route_edit/', views.route_edit, name='route_edit'),
    path('<int:route_id>/solve', views.solve, name="solve"),
    path('<int:route_id>/result', views.result, name="result")
]