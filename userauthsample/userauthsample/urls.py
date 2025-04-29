"""
URL configuration for userauthsample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authsample import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('authsample.urls')),
    path("", views.top, name='top'),
    path("accounts/", include("accounts.urls")),
    path("salesman_new/", views.salesman_new, name="salesman_new"),
    path('<uuid:salesman_id>/salesmen_detail/', views.salesman_detail, name='salesman_detail'),
    path('<uuid:salesman_id>/salesman_edit/', views.salesman_edit, name='salesman_edit'),
    path('city_new/', views.city_new, name='city_new'),
    path('<uuid:city_id>/city_detail/', views.city_detail, name='city_detail'),
    path('<uuid:city_id>/city_edit/', views.city_edit, name='city_edit'),
    path('route_new/', views.route_new, name='route_new'),
    path('<uuid:route_id>/route_detail/', views.route_detail, name='route_detail'),
    path('<uuid:route_id>/route_edit/', views.route_edit, name='route_edit'),
    path('solve/<uuid:route_id>/', views.solve, name='solve'),
]