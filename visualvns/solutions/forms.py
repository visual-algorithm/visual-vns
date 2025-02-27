from django import forms
from django.forms import modelformset_factory
from solutions.models import City, Salesman, Route

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name', 'address', 'description')

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ["name", "city"]

class RouteForm(forms.ModelForm):
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Cities"
    )

    class Meta:
        model= Route
        fields = ["name", "cities"]

