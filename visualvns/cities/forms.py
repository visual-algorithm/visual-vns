from django import forms
from cities.models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name', 'address', 'description', 'salesman')