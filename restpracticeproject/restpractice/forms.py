from django import forms
from .models import Salesman, City, Route

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ('name', 'description')

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'address', 'salesman', 'description')

class RouteForm(forms.ModelForm):
    salesmen = forms.ModelMultipleChoiceField(
        queryset=Salesman.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Salesmen"
    )
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Cities"
    )
    class Meta:
        model = Route
        fields = ('name', 'depot', 'cities', 'salesmen', 'description')

# class RouteForm(forms.ModelForm):
