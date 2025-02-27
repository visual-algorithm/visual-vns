from django.urls import path

from solutions import views


urlpatterns = [
    path('new/', views.city_new, name='city_new'),
    path('<int:city_id>/', views.city_detail, name='city_detail'),
    path('<int:city_id>/edit/', views.city_edit, name='city_edit'),
    path('solve_prepare/', views.solve_prepare, name='solve_prepare'),
    path('solve', views.solve, name='solve'),
    
]