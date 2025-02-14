from django.urls import path

from routes import views

urlpatterns = [
    path("new/", views.route_new, name="route_new"),
    path("<int:route_id>/", views.route_detail, name="route_detail"),
    path("<int:route_id>/edit/", views.route_edit, name="route_edit"),
]