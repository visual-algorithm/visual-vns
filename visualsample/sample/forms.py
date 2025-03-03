from django import forms
from .models import City, Salesman, Route

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['name']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'salesman']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'cities', 'salesmen']
