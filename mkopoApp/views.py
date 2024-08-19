from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Loan, LoanPayment
from .forms import LoanRequestForm
from django.contrib import messages
from .serializers import LoanSerializer

@login_required(login_url='/account/login/')
def loan_request_view(request):
    # Check if there is any active loan
    active_loan = Loan.objects.filter(user=request.user, status='Approved').exists()
    if active_loan:
        messages.error(request, 'You still have an active loan. Finish loan payment to request another loan.')
        return render(request, 'mkopoApp/loan_request.html', {
            'form': LoanRequestForm(),  # Provide a fresh form
            'loans': Loan.objects.filter(user=request.user),
            'payments': LoanPayment.objects.filter(loan__user=request.user).order_by('year', 'month'),
        })

    # Check if there is a pending loan request
    pending_request = Loan.objects.filter(user=request.user, status='Pending').exists()
    if pending_request:
        messages.error(request, 'You have already submitted a loan request. Please wait for it to be processed before submitting another.')
        return render(request, 'mkopoApp/loan_request.html', {
            'form': LoanRequestForm(),  # Provide a fresh form
            'loans': Loan.objects.filter(user=request.user),
            'payments': LoanPayment.objects.filter(loan__user=request.user).order_by('year', 'month'),
        })

    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > 10000000:
                messages.error(request, 'The maximum loan amount is Tsh 10,000,000.')
            else:
                loan_data = {
                    'user': request.user,  # Directly using the user object
                    'amount': amount,
                    'status': 'Pending',
                }
                serializer = LoanSerializer(data=loan_data)
                if serializer.is_valid():
                    serializer.save()
                    messages.success(request, 'Loan request submitted successfully.')
                    return redirect('mkopo_App:loan_request')
                else:
                    messages.error(request, 'Error submitting loan request.')
        else:
            messages.error(request, 'There was an error in your form submission.')
    else:
        form = LoanRequestForm()

    return render(request, 'mkopoApp/loan_request.html', {
        'form': form,
        'loans': Loan.objects.filter(user=request.user),
        'payments': LoanPayment.objects.filter(loan__user=request.user).order_by('year', 'month'),
    })

@login_required(login_url='/account/login/')
def member_loan_payments_view(request):
    # Get the current approved loan for the user
    current_loan = Loan.objects.filter(user=request.user, status='Approved').order_by('-date').first()

    if not current_loan:
        # Handle case where no approved loans are found
        messages.error(request, 'You have no active loan.')
        return render(request, 'mkopoApp/loan_request.html', {
            'form': LoanRequestForm(),
            'loans': Loan.objects.filter(user=request.user),
        })

    # Get all payments related to the current loan
    payments = LoanPayment.objects.filter(loan=current_loan).order_by('year', 'month')

    context = {
        'current_loan': current_loan,
        'payments': payments,
    }

    return render(request, 'mkopoApp/loan_payments.html', context)
