from django import forms

from routes.models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('title', 'depot', 
                  'spot1', 'spot2', 'spot3',
                  'spot4', 'spot5', 'spot6',
                  'spot7', 'spot8', 'spot9',
                  'spot10', 'spot11', 'spot12',
                  'spot13', 'spot14', 'spot15',
                  'spot16', 'spot17', 'spot18',
                  'spot19', 'spot20',
                  'description')