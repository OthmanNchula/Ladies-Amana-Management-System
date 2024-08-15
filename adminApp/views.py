from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from mkopoApp.models import Loan, LoanPayment
from mtajiApp.models import Mtaji
from michangoApp.models import Michango
from swadaqaApp.models import Swadaqa
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Sum, Case, When
from django.db.models import Sum, Case, When, Value, DecimalField
from django.contrib.auth import get_user_model
from adminApp.models import PendingChanges, ActivityLog
from django.http import HttpResponse
from django.utils import timezone


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
    # Fetch the user by ID
    user = get_object_or_404(User, id=user_id)

    # Start with the 'loans' data
    loans = Loan.objects.filter(user=user)
    mtaji = Mtaji.objects.filter(user=user)
    michango = Michango.objects.filter(user=user)
    swadaqa = Swadaqa.objects.filter(user=user)
    
    # Check if it works fine with just loans
    context = {
        'managed_user': user,
        'loans': loans,
        'mtaji': mtaji,
        'michango': michango,
        'swadaqa': swadaqa,
        
        'show_back_button': True,
    }
    return render(request, 'adminApp/manage_dashboard.html', context)

# Mtaji
@login_required(login_url='/account/login/')
def manage_mtaji(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Assuming you have a Mtaji model that tracks contributions by year
    mtaji_data = Mtaji.objects.filter(user=user)

    # Create a list of years, you may customize this part
    years = [year for year in range(2018, 2025)]
    current_year = years[-1]  # Default to the most recent year

    # If a POST request is made, handle the form submission
    if request.method == 'POST':
        year = request.POST.get('amount_{}'.format(current_year))
        amount = request.POST.get('amount_{}'.format(current_year), 0)
        
        # Update or create Mtaji record for the current year
        mtaji_record, created = Mtaji.objects.update_or_create(
            user=user, year=current_year,
            defaults={'amount': amount}
        )

    context = {
        'managed_user': user,
        'years': years,
        'current_year': current_year,
        'mtaji_data': mtaji_data,
        'show_back_button': True,
    }
    return render(request, 'adminApp/manage_mtaji.html', context)
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
    # if not isinstance(data['amount'], (int, float)) or not isinstance(data['total'], (int, float)):
    #     return JsonResponse({'error': 'Non-serializable data encountered'}, status=400)
    # return JsonResponse(data)
    
@login_required(login_url='/account/login/')
def manage_mchango(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_year = timezone.now().year
    
    # Fetch Michango data for the selected user and year
    selected_year = int(request.GET.get('year', current_year))
    michango_entries = Michango.objects.filter(user=user, year=selected_year)

    # Define months in Kiswahili
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    months_with_data = {month: michango_entries.get(month=index+1).amount if michango_entries.filter(month=index+1).exists() else 0 for index, month in enumerate(months)}

    context = {
        'managed_user': user,
        'current_year': selected_year,
        'years': range(2018, timezone.now().year + 1),
        'months_with_data': months_with_data.items(),
        'show_back_button': True,
    }
    
    return render(request, 'adminApp/manage_mchango.html', context)

@login_required(login_url='/account/login/')
def save_mchango(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_year = int(request.GET.get('year', timezone.now().year))
    
    # Define months in Kiswahili
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if request.method == 'POST':
        for month in months:
            amount = request.POST.get(f'amount_{month}')
            month_number = months.index(month) + 1  # Convert month name to month number
            michango, created = Michango.objects.update_or_create(
                user=user,
                year=current_year,
                month=month_number,
                defaults={'amount': amount}
            )
        return redirect('admin_App:manage_mchango', user_id=user.id)

    return redirect('admin_App:manage_user', user_id=user.id)

@login_required(login_url='/account/login/')
def manage_swadaqa(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Fetch Swadaqa data for the user
    swadaqa_data = Swadaqa.objects.filter(user=user)

    # Create a list of years
    years = [year for year in range(2018, timezone.now().year + 1)]
    current_year = years[-1]  # Default to the most recent year

    # Handle form submission
    if request.method == 'POST':
        year = request.POST.get('amount_{}'.format(current_year))
        amount = request.POST.get('amount_{}'.format(current_year), 0)
        
        # Update or create Swadaqa record for the current year
        swadaqa_record, created = Swadaqa.objects.update_or_create(
            user=user, year=current_year,
            defaults={'amount': amount}
        )

    context = {
        'managed_user': user,
        'years': years,
        'current_year': current_year,
        'swadaqa_data': swadaqa_data,
        'show_back_button': True,
    }
    return render(request, 'adminApp/manage_swadaqa.html', context)

@login_required
def swadaqa_data(request, user_id, year):
    user = get_object_or_404(User, id=user_id)
    try:
        swadaqa = Swadaqa.objects.get(user=user, year=year)
        amount = swadaqa.amount
    except Swadaqa.DoesNotExist:
        amount = 0

    data = {
        'year': year,
        'amount': amount,
        'total': amount
    }
    
    return JsonResponse(data)

@login_required(login_url='/account/login/')
def manage_mkopo(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Step 1: Check loan status
    try:
        current_loan = Loan.objects.get(user=user, status='Approved')
        loan_status = 'Active'
    except Loan.DoesNotExist:
        current_loan = None
        loan_status = 'Inactive'

    # Step 2: Loan Limit Message
    loan_limit = 10000000  # Example loan limit

    # Step 3: Check if there's a pending loan request
    try:
        loan_request = Loan.objects.get(user=user, status='Pending')
        has_request = True
    except Loan.DoesNotExist:
        loan_request = None
        has_request = False

    # Step 4: Loan History
    loan_history = Loan.objects.filter(user=user).exclude(status='Pending')

    # Step 5: Loan Payments
    loan_payments = []
    if current_loan:
        start_date = current_loan.date + timedelta(days=30)  # Payment starts 1 month after approval
        for i in range(36):  # 36 payments for 36 months
            payment_year = start_date.year + (start_date.month + i - 1) // 12
            payment_month = (start_date.month + i - 1) % 12 + 1
            payment = LoanPayment.objects.filter(loan=current_loan, year=payment_year, month=payment_month).first()
            loan_payments.append({
                'year': payment_year,
                'month': payment_month,
                'amount': payment.amount if payment else 0
            })

    context = {
        'managed_user': user,
        'loan_status': loan_status,
        'loan_limit': loan_limit,
        'has_request': has_request,
        'loan_request': loan_request,
        'loan_history': loan_history,
        'current_loan': current_loan,
        'loan_payments': loan_payments,
        'show_back_button': True,
    }

    return render(request, 'adminApp/manage_mkopo.html', context)

def process_loan_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        decision = request.POST.get('decision')
        loan_request = get_object_or_404(Loan, user=user, status='Pending')

        if decision == 'accept':
            # Accept the loan request
            loan_request.status = 'Approved'
            loan_request.date = timezone.now()  # Update the date to the approval date
            loan_request.save()
        elif decision == 'reject':
            # Reject the loan request
            loan_request.status = 'Rejected'
            loan_request.save()
        
    return redirect('admin_App:manage_mkopo', user_id=user.id)

@login_required(login_url='/account/login/')
def loan_payments_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_loan = get_object_or_404(Loan, user=user, status='Approved')

    # Calculate the start and end dates for the 36-month period
    start_date = current_loan.date + timedelta(days=30)  # Loan payment starts one month after approval
    end_date = start_date + timedelta(days=36*30)  # 36 months period

    # Prepare payment schedule
    payments_schedule = []
    current_date = start_date

    for _ in range(36):
        year = current_date.year
        month = current_date.month
        payments = LoanPayment.objects.filter(loan=current_loan, payment_date__year=year, payment_date__month=month)
        total_paid = sum(payment.amount for payment in payments)
        
        payments_schedule.append({
            'year': year,
            'month': month,
            'total_paid': total_paid,
            'payments': payments,
        })
        
        current_date += timedelta(days=30)  # Move to the next month

    context = {
        'managed_user': user,
        'current_loan': current_loan,
        'payments_schedule': payments_schedule,
        'show_back_button': True,
    }
    
    return render(request, 'adminApp/loan_payments.html', context)
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
@login_required(login_url='/account/login/')
def members_loans(request):
    # Get the current year
    current_year = datetime.now().year
    
    # Get the selected year from the request (default to current year)
    selected_year = int(request.GET.get('year', current_year))
    
    # Fetch all members and their loan status
    members = User.objects.filter(is_staff=False, is_superuser=False).annotate(
        total_loan=Sum(
            Case(
                When(loan__status='Approved', loan__date__year=selected_year, then='loan__amount'),
                default=Value(0),
                output_field=DecimalField()
            )
        )
    )

    # Prepare a list of members with their loan status and amount
    members_loans_info = []
    for member in members:
        loan = Loan.objects.filter(user=member, status='Approved', date__year=selected_year).first()
        loan_status = 'No Loan' if loan is None else 'Approved'
        loan_amount = 0 if loan is None else loan.amount
        members_loans_info.append({
            'username': member.username,
            'phone_number': member.profile.phone_number,
            'loan_status': loan_status,
            'loan_amount': loan_amount
        })

    # Calculate the total amount of loans taken in the selected year
    total_loans = Loan.objects.filter(status='Approved', date__year=selected_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Generate a list of years for the dropdown (e.g., from 2018 to the current year)
    years = list(range(2018, current_year + 1))

    context = {
        'members_loans_info': members_loans_info,
        'total_loans': total_loans,
        'years': years,
        'selected_year': selected_year,
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
