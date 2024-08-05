from django import forms
from .models import Mtaji


class MtajiForm(forms.ModelForm):
    class Meta:
        model = Mtaji
        fields = ['user', 'year', 'amount']