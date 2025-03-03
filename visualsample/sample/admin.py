from django.contrib import admin
from .models import City, Salesman, Route

# Register your models here.

admin.site.register(Salesman)
admin.site.register(City)
admin.site.register(Route)