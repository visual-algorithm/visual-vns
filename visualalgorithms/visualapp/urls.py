from django.urls import path
from visualapp import views

urlpatterns = [
    path("<new/", views.cource_new, name="cource_new"),
    path("<int:cource_id>/", views.cource_detail, name="cource_detail"),
    path("<int:cource_id>/edit/", views.cource_edit, name="cource_edit")
]