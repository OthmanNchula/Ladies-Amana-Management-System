# michangoApp/forms.py
from django import forms
from .models import Michango

class MichangoForm(forms.ModelForm):
    class Meta:
        model = Michango
        fields = ['screenshot']  # Only allow uploading screenshots in this form
