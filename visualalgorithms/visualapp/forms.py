from django import forms
from visualapp.models import Cource

class CourceForm(forms.ModelForm):
    class Meta:
        model = Cource
        fields = ('title', 'start', 'spot1', 'spot2', 'spot3')