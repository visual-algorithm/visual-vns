from django import forms
from django.forms import modelformset_factory
from cities.models import City, Salesman

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name', 'address', 'description')

class SolveForm(forms.Form):
    salesman = forms.ModelChoiceField(
        queryset=Salesman.objects.all(),
        required=True,
        label="巡回させるセールスマン"
    )
    class Meta:
        model = City
        fields = ["city", "salesman"]
        widgets = {"city": forms.HiddenInput()}

CityFormSet = modelformset_factory(
    City,
    form = CityForm,
    extra=0
)