# adminApp/forms.py

from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from loginApp.models import Profile  # Import the Profile model

class AddMemberForm(forms.ModelForm):
    full_name = forms.CharField(max_length=60, required=True)
    one_time_password = forms.CharField(
        max_length=20,
        required=False,
        help_text="Leave blank to auto-generate a random password."
    )

    class Meta:
        model = User
        fields = ['full_name', 'one_time_password']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Split the full name into first and last name
        full_name = self.cleaned_data['full_name'].strip().split()
        user.first_name = full_name[0]
        user.last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ""

        # Generate a unique username and store it in the profile for reference
        base_username = f"{user.first_name}{user.last_name}".replace(" ", "").lower()
        user.username = base_username  # Removed random part

        # Generate or use provided one-time password
        one_time_password = self.cleaned_data.get('one_time_password')
        user.set_password(one_time_password or get_random_string(8))

        if commit:
            user.save()

            # Ensure profile is created and save the full_name and must_change_password flag
            profile, created = Profile.objects.get_or_create(user=user)
            profile.full_name = self.cleaned_data['full_name']
            profile.must_change_password = True
            profile.save()

        return user
