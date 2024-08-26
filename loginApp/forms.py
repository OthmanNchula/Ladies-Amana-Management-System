from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PaymentScreenshot


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    nida = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Female', 'Female'), ('Male', 'Male')], required=False)
    next_of_kin_first_name = forms.CharField(max_length=30, required=False)
    next_of_kin_last_name = forms.CharField(max_length=30, required=False)
    next_of_kin_phone_number = forms.CharField(max_length=15, required=False)

    class Meta: 
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name', 'nida', 'birth_date', 'gender', 'next_of_kin_first_name', 'next_of_kin_last_name', 'next_of_kin_phone_number']

        
class UserLoginForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')

class EditInfoForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    nida = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    next_of_kin_first_name = forms.CharField(max_length=30, required=False)
    next_of_kin_last_name = forms.CharField(max_length=30, required=False)
    next_of_kin_phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'nida', 'birth_date', 'next_of_kin_first_name', 'next_of_kin_last_name', 'next_of_kin_phone_number']


class PaymentScreenshotForm(forms.ModelForm):
    class Meta:
        model = PaymentScreenshot
        fields = ['image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a brief description'}),
        }
