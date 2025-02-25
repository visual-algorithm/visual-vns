from django import forms
from cities.models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name', 'address', 'description', 'salesman')

class SolveForm(forms.Form):
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"onchange": "this.form.submit();"}),
        required = True,
        label="選択してください",
    )