from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Loan
from .forms import LoanRequestForm
from django.contrib import messages


@login_required(login_url='/account/login/')
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > 10000000:
                messages.error(request, 'The maximum loan amount is Tsh 10,000,000.')
            else:
                Loan.objects.create(user=request.user, amount=amount, status='Pending')
                messages.success(request, 'Loan request submitted successfully.')
                return redirect('mkopo_App:loan_request')
    else:
        form = LoanRequestForm()

    loans = Loan.objects.filter(user=request.user)

    return render(request, 'mkopoApp/loan_request.html', {
        'form': form,
        'loans': loans
    })
