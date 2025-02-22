from django.urls import path

from cities import views


urlpatterns = [
    path('new/', views.cities_new, name='cities_new'),
    path('<int:cities_id>/', views.cities_detail, name='cities_detail'),
    path('<int:cities_id>/edit/', views.cities_edit, name='cities_edit'),
]