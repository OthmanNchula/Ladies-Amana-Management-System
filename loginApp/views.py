from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import EditInfoForm
from .models import Profile

def generate_unique_username(first_name, last_name):
    base_username = f"{first_name}_{last_name}"
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

# Registration view
def register(request):
    error = ''
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_unique_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'phone_number': form.cleaned_data['phone_number'],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'nida': form.cleaned_data['nida'],
                    'birth_date': form.cleaned_data['birth_date'],
                    'gender': form.cleaned_data['gender'],
                    'next_of_kin_first_name': form.cleaned_data['next_of_kin_first_name'],
                    'next_of_kin_last_name': form.cleaned_data['next_of_kin_last_name'],
                    'next_of_kin_phone_number': form.cleaned_data['next_of_kin_phone_number'],
                }
            )
            messages.success(request, 'User registered successfully')

            password = form.cleaned_data['password1']
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('login_App:user_dashboard'))
            
            return HttpResponseRedirect(reverse('login_App:login'))
        else:
            error = 'Your password is not strong enough or both passwords must be the same'

    return render(request, 'loginApp/register.html', context={'form': form, 'error': error})

# Login view
def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = f"{first_name}_{last_name}"
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('login_App:user_dashboard'))
            else:
                messages.error(request, 'Invalid first name, last name or password')
    return render(request, 'loginApp/login.html', context={'form': form})

# User dashboard view
@login_required(login_url='/account/login/')
def user_dashboard(request):
    return render(request, 'loginApp/user_dashboard.html')

@login_required
def edit_info(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = EditInfoForm(request.POST, instance=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.nida = form.cleaned_data['nida']
            profile.birth_date = form.cleaned_data['birth_date']
            profile.next_of_kin_first_name = form.cleaned_data['next_of_kin_first_name']
            profile.next_of_kin_last_name = form.cleaned_data['next_of_kin_last_name']
            profile.next_of_kin_phone_number = form.cleaned_data['next_of_kin_phone_number']
            user.save()
            profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('login_App:edit_info')
    else:
        form = EditInfoForm(instance=user)
        form.fields['phone_number'].initial = profile.phone_number
    return render(request, 'loginApp/edit_info.html', {'form': form})
