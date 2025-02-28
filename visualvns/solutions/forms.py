from django import forms
from django.forms import modelformset_factory
from solutions.models import City, Salesman, Route

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name', 'address', 'salesman', 'description')

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ["salesman_name"]

class RouteForm(forms.ModelForm):
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Cities"
    )

    class Meta:
        model= Route
        fields = ["route_name", "depot", "cities", "route_description"]

