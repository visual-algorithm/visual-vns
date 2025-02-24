from django.contrib import admin
from cities.models import City, Route, Salesman

# Register your models here.

admin.site.register(City)
admin.site.register(Route)
admin.site.register(Salesman)
