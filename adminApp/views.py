from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from mkopoApp.models import Loan
from mtajiApp.models import Mtaji
from michangoApp.models import Michango
from swadaqaApp.models import Swadaqa
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Sum, Case, When
from django.db.models import Sum, Case, When, Value, DecimalField
from django.contrib.auth import get_user_model
from adminApp.models import PendingChanges, ActivityLog
import logging


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_App:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    return render(request, 'adminApp/admin_login.html')

def admin_dashboard(request):
    context = get_dashboard_context()
    context['show_back_button'] = False
    return render(request, 'adminApp/dashboard.html', context)

def get_dashboard_context():
    total_members = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_mtaji = Mtaji.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_michango = Michango.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_swadaqa = Swadaqa.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loans = Loan.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    loan_requests = Loan.objects.filter(status='Pending').count()
    approved_loans = Loan.objects.filter(status='Approved').count()
    rejected_loans = Loan.objects.filter(status='Rejected').count()

    context = {
        'total_members': total_members,
        'total_mtaji': total_mtaji,
        'total_michango': total_michango,
        'total_swadaqa': total_swadaqa,
        'total_loans': total_loans,
        'loan_requests': loan_requests,
        'approved_loans': approved_loans,
        'rejected_loans': rejected_loans,
    }
    return context

def superuser_login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_App:admin_dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_App:admin_dashboard')
                else:
                    messages.error(request, 'You are not a Super User')
            else:
                messages.error(request, 'Invalid Username or Password')
    return render(request, 'adminApp/admin_login.html')

#members
@login_required(login_url='/account/login/')
def members(request):
    members = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'adminApp/members.html', {'users': members, 'show_back_button': False})

@login_required(login_url='/account/login/')
def manage_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Fetch data relevant to the user
    loans = Loan.objects.filter(user=user)
    mtaji = Mtaji.objects.filter(user=user)
    michango = Michango.objects.filter(user=user)
    swadaqa = Swadaqa.objects.filter(user=user)

    context = {
        'user': user,
        'loans': loans,
        'mtaji': mtaji,
        'michango': michango,
        'swadaqa': swadaqa,
        'show_back_button': True,  # This can be toggled if you want to include a back button
    }
    # Render the manage_dashboard.html within the admin_base.html layout
    return render(request, 'adminApp/manage_dashboard.html', context)


# Mtaji
logger = logging.getLogger(__name__)
@login_required(login_url='/adminApp/login/')
def manage_mtaji(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))

    if request.method == 'POST':
        for year in years:
            amount_key = f"amount_{year}"
            if amount_key in request.POST:
                try:
                    amount = int(request.POST.get(amount_key, 0))
                except ValueError:
                    amount = 0

                try:
                    # Fetch or create the Mtaji object
                    mtaji, created = Mtaji.objects.get_or_create(user=user, year=year)
                    mtaji.amount = amount
                    mtaji.save()

                    # Log the action
                    if created:
                        logger.info(f"Created new Mtaji for user {user.username} for year {year}.")
                    else:
                        logger.info(f"Updated Mtaji for user {user.username} for year {year}.")
                
                except Exception as e:
                    # Log the error for debugging
                    logger.error(f"Error occurred while handling Mtaji for user {user.username} for year {year}: {str(e)}")
                    # Consider adding additional error handling here

    return render(request, 'adminApp/manage_mtaji.html', {
        'user': user,
        'current_year': current_year,
        'years': years,
    })

@login_required
def mtaji_data(request, user_id, year):
    user = get_object_or_404(User, id=user_id)
    try:
        mtaji = Mtaji.objects.get(user=user, year=year)
        amount = mtaji.amount
    except Mtaji.DoesNotExist:
        amount = 0

    data = {
        'year': year,
        'amount': amount,
        'total': amount  # This should also be a simple number
    }
    
    # Check for non-serializable types before returning
    if not isinstance(data['amount'], (int, float)) or not isinstance(data['total'], (int, float)):
        return JsonResponse({'error': 'Non-serializable data encountered'}, status=400)

    return JsonResponse(data)

@login_required(login_url='/account/login/')
def mitaji_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))
    selected_year = int(request.GET.get('year', current_year))

    total_mtaji = Mtaji.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_mtaji_year = Mtaji.objects.filter(year=selected_year).aggregate(Sum('amount'))['amount__sum'] or 0
    members = User.objects.filter(is_staff=False, is_superuser=False)
    
    members_mtaji = []
    for member in members:
        mtaji = Mtaji.objects.filter(user=member, year=selected_year).first()
        amount = mtaji.amount if mtaji else 0
        members_mtaji.append({
            'username': member.username,
            'amount': amount
        })

    context = {
        'total_mtaji': total_mtaji,
        'total_mtaji_year': total_mtaji_year,
        'years': years,
        'selected_year': selected_year,
        'members_mtaji': members_mtaji
    }

    return render(request, 'adminApp/mitaji.html', context)

#Michango
@login_required
def michango_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Fetch total michango
    total_michango = Michango.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    members = User.objects.filter(is_staff=False, is_superuser=False)
    selected_year = int(request.GET.get('year', current_year))
    total_year_michango = Michango.objects.filter(year=selected_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch michango data for each month in the selected year
    total_michango_by_month = {month: Michango.objects.filter(year=selected_year, month=i+1).aggregate(Sum('amount'))['amount__sum'] or 0 for i, month in enumerate(months)}

    members_michango = []
    for member in members:
        member_michango_by_month = {
            month: Michango.objects.filter(user=member, year=selected_year, month=i+1).aggregate(Sum('amount'))['amount__sum'] or 0 for i, month in enumerate(months)
        }
        members_michango.append({
            'username': member.username,
            'michango_by_month': member_michango_by_month
        })

    context = {
        'total_michango': total_michango,
        'total_year_michango': total_year_michango,
        'total_michango_by_month': total_michango_by_month,
        'years': years,
        'selected_year': selected_year,
        'months': months,
        'members_michango': members_michango
    }

    return render(request, 'adminApp/michango.html', context)



#loans
@login_required
def members_loans(request):
    # Fetch all members and their loan status
    members = User.objects.filter(is_staff=False, is_superuser=False).annotate(
        total_loan=Sum(
            Case(
                When(loan__status='Approved', then='loan__amount'),
                default=Value(0),
                output_field=DecimalField()
            )
        )
    )

    # Prepare a list of members with their loan status and amount
    members_loans_info = []
    for member in members:
        loan = Loan.objects.filter(user=member, status='Approved').first()
        loan_status = 'No Loan' if loan is None else 'Approved'
        loan_amount = 0 if loan is None else loan.amount
        members_loans_info.append({
            'username': member.username,
            'phone_number': member.profile.phone_number,
            'loan_status': loan_status,
            'loan_amount': loan_amount
        })

    # Calculate the total amount of loans taken
    total_loans = Loan.objects.filter(status='Approved').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'members_loans_info': members_loans_info,
        'total_loans': total_loans,
    }

    return render(request, 'adminApp/members_loans.html', context)


@login_required(login_url='/account/login/')
def loan_requests(request):
    loan_requests = Loan.objects.filter(status='Pending')
    return render(request, 'adminApp/loan_requests.html', {'loans': loan_requests, 'show_back_button': False})

@login_required(login_url='/account/login/')
def approved_loans(request):
    approved_loans = Loan.objects.filter(status='Approved')
    return render(request, 'adminApp/approved_loans.html', {'loans': approved_loans, 'show_back_button': False})

@login_required(login_url='/account/login/')
def rejected_loans(request):
    rejected_loans = Loan.objects.filter(status='Rejected')
    return render(request, 'adminApp/rejected_loans.html', {'loans': rejected_loans, 'show_back_button': False})

@login_required(login_url='/account/login/')
def approve_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = 'Approved'
    loan.save()
    messages.success(request, 'Loan approved successfully.')
    return redirect('admin_App:loan_requests')

@login_required(login_url='/account/login/')
def reject_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = 'Rejected'
    loan.save()
    messages.success(request, 'Loan rejected successfully.')
    return redirect('admin_App:loan_requests')


# verification for admin1
@login_required(login_url='/account/login/')
def verification(request):
    if request.user.username == 'admin1':
        if request.method == 'POST':
            password = request.POST.get('password')
            primary_admin = authenticate(username=request.user.username, password=password)
            if primary_admin is not None:
                pending_changes = PendingChanges.objects.filter(is_approved=False)
                return render(request, 'adminApp/verification.html', {'pending_changes': pending_changes})
            else:
                messages.error(request, 'Invalid password.')
                return redirect('admin_App:verification')
        return render(request, 'adminApp/password_prompt.html')
    else:
        messages.error(request, 'Access denied.')
        return redirect('admin_App:admin_dashboard')

@login_required(login_url='/account/login/')
def approve_change(request, change_id):
    if request.user.username == 'admin1':
        pending_change = get_object_or_404(PendingChanges, id=change_id)
        pending_change.is_approved = True
        pending_change.approved_by = request.user
        pending_change.save()

        ActivityLog.objects.create(
            admin=request.user,
            action=f"Approved {pending_change.action}",
            details=f"Approved changes to {pending_change.table_name}"
        )

        messages.success(request, 'Change approved successfully.')
    return redirect('admin_App:verification')

@login_required(login_url='/account/login/')
def reject_change(request, change_id):
    if request.user.username == 'admin1':
        pending_change = get_object_or_404(PendingChanges, id=change_id)
        pending_change.delete()

        ActivityLog.objects.create(
            admin=request.user,
            action=f"Rejected {pending_change.action}",
            details=f"Rejected changes to {pending_change.table_name}"
        )

        messages.success(request, 'Change rejected successfully.')
    return redirect('admin_App:verification')

@login_required(login_url='/account/login/')
def verified_actions(request):
    verified_actions = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'adminApp/verified_actions.html', {'verified_actions': verified_actions})

# mengineyo
@login_required(login_url='/account/login/')
def mengineyo(request):
    
    return render(request, 'adminApp/mengineyo.html')
