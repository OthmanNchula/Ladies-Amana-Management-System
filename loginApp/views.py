from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import EditInfoForm
from .models import Profile
from .forms import PaymentScreenshotForm
from .models import PaymentScreenshot
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from adminApp.models import Notification
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mtajiApp.models import Mtaji
from michangoApp.models import Michango
from swadaqaApp.models import Swadaqa
from mkopoApp.models import Loan


def generate_unique_username(first_name, last_name):
    base_username = f"{first_name}_{last_name}"
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

# Login view

def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # Use full name to get the actual username
            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']

            # Fetch the user profile based on full_name
            try:
                profile = Profile.objects.get(full_name=full_name)
                username = profile.user.username
            except Profile.DoesNotExist:
                messages.error(request, 'Invalid full name or password')
                return render(request, 'loginApp/login.html', context={'form': form, 'is_login_page': True})

            # Authenticate using the fetched username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Check if this is the first login and prompt for password change if needed
                if user.profile.must_change_password:
                    return redirect('login_App:change_password_prompt')

                return redirect(reverse('login_App:user_dashboard'))
            else:
                messages.error(request, 'Invalid full name or password')
    return render(request, 'loginApp/login.html', context={'form': form, 'is_login_page': True})



@login_required(login_url='/account/login/')
def change_password_prompt(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            # Mark the password as no longer needing change
            user.profile.must_change_password = False
            user.profile.save()
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('login_App:edit_info')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'loginApp/change_password_prompt.html', {'form': form})

# User dashboard view
@login_required(login_url='/account/login/')
def user_dashboard(request):
    # Get the logged-in user
    user = request.usere

    # Calculate totals for Mtaji, Michango, and Swadaqa
    total_mtaji = Mtaji.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_mchango = Michango.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_swadaqa = Swadaqa.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        
    # Pass data to the template
    context = {
        'user': user,
        'total_mtaji': total_mtaji,
        'total_mchango': total_mchango,
        'total_swadaqa': total_swadaqa,
    }
    return render(request, 'loginApp/user_dashboard.html', context)


@login_required
def edit_info(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = EditInfoForm(request.POST, instance=user)
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].strip().split()
            user.first_name = full_name[0]
            user.last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ""
            user.email = form.cleaned_data['email']
            user.save()

            # Update Profile-specific fields
            profile.phone_number = form.cleaned_data['phone_number']
            profile.nida = form.cleaned_data['nida']
            profile.birth_date = form.cleaned_data['birth_date']
            profile.next_of_kin_first_name = form.cleaned_data['next_of_kin_first_name']
            profile.next_of_kin_last_name = form.cleaned_data['next_of_kin_last_name']
            profile.next_of_kin_phone_number = form.cleaned_data['next_of_kin_phone_number']
            profile.full_name = f"{user.first_name} {user.last_name}"
            profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('login_App:user_dashboard')
    else:
        # Pre-fill full_name as a single string
        initial_full_name = f"{user.first_name} {user.last_name}".strip()
        form = EditInfoForm(instance=profile, initial={'full_name': initial_full_name})
    
    return render(request, 'loginApp/edit_info.html', {'form': form})

@login_required(login_url='/account/login/')
def upload_payment_image(request):
    if request.method == 'POST':
        form = PaymentScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            payment_screenshot = form.save(commit=False)
            payment_screenshot.user = request.user
            payment_screenshot.save()
            
             # Create notifications for all admins
            admins = User.objects.filter(is_staff=True)
            for admin in admins:
                Notification.objects.create(
                    admin=admin,
                    message=f"New payment image uploaded by {request.user.username}",
                    payment_screenshot=payment_screenshot
                )
                
            messages.success(request, 'Image uploaded successfully.')
            return render(request, 'loginApp/user_dashboard.html', {'form': form}) # Redirect to user dashboard or another page
    else:
        form = PaymentScreenshotForm()
    return render(request, 'loginApp/upload_payment_image.html', {'form': form})

@login_required(login_url='/account/login/')
def payment_images(request):
    payment_images = PaymentScreenshot.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'payment_images': payment_images,
        'show_back_button': True
    }
    return render(request, 'loginApp/payment_images.html', context)

@login_required(login_url='/account/login/')
def delete_payment_image(request, image_id):
    image = get_object_or_404(PaymentScreenshot, id=image_id, user=request.user)

    if request.method == "POST":
        image.delete()
        messages.success(request, "Payment screenshot deleted successfully.")

    return redirect('login_App:payment_images')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'loginApp/password_reset_form.html'
    success_url = reverse_lazy('login_App:password_reset_complete')
