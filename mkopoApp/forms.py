from django import forms
from .models import Loan

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingiza Kiasi Cha Mkopo',
                'max': 10000000,
                'min': 1,
            })
        }
        labels = {
            'amount': 'Amount (Tsh)',
        }
