from django import forms
from .models import Salesman, City

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['name', 'description']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'address', 'salesman', 'description']
