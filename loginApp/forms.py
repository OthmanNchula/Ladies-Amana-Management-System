from django import forms
from django.contrib.auth.models import User
from .models import PaymentScreenshot


class UserLoginForm(forms.Form):
    full_name = forms.CharField(max_length=150, label="Full name")  # Should match template
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        fields = ['full_name', 'password']

class EditInfoForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    full_name = forms.CharField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make the field read-only
    )
    nida = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    next_of_kin_first_name = forms.CharField(max_length=30, required=False)
    next_of_kin_last_name = forms.CharField(max_length=30, required=False)
    next_of_kin_phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name' , 'nida', 'birth_date', 'next_of_kin_first_name', 'next_of_kin_last_name', 'next_of_kin_phone_number']


class PaymentScreenshotForm(forms.ModelForm):
    class Meta:
        model = PaymentScreenshot
        fields = ['image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter a brief description',
                'style': 'width: 100%; max-width: 100%;'  # Ensures it fits within container width
            }),
        }