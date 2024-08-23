# michangoApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Michango
from .forms import MichangoForm
from datetime import datetime
from django.http import JsonResponse
from django.core.files.storage import default_storage

@login_required(login_url='/account/login/')
def mchango_view(request):
    current_year = datetime.now().year
    selected_year = int(request.GET.get('year', current_year))  # Get the selected year from the URL, default to the current year
    years = list(range(2018, current_year + 1))
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    contributions = Michango.objects.filter(user=request.user)

    # Calculate the total for the selected year
    total_mchango_year = contributions.filter(year=selected_year).aggregate(total=Sum('amount'))['total'] or 0
    total_mchango_all_years = contributions.aggregate(total=Sum('amount'))['total'] or 0

    data_by_year = {}
    for year in years:
        yearly_contributions = contributions.filter(year=year)
        data_by_year[year] = {contribution.month: contribution for contribution in yearly_contributions}

    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        michango_instance, created = Michango.objects.get_or_create(user=request.user, year=year, month=month)
        form = MichangoForm(request.POST, request.FILES, instance=michango_instance)
        if form.is_valid():
            form.save()
            return redirect('michango_App:mchango')
    else:
        form = MichangoForm()

    return render(request, 'michangoApp/mchango.html', {
        'current_year': current_year,
        'selected_year': selected_year,  # Pass the selected year to the template
        'years': years,
        'data_by_year': data_by_year,
        'months': month_names,
        'total_mchango_year': total_mchango_year,
        'total_mchango_all_years': total_mchango_all_years,
        'form': form,  # Pass the form to the template
    })

@login_required(login_url='/account/login/')
def mchango_data(request, year):
    contributions = Michango.objects.filter(user=request.user, year=year)
    data = {contribution.month: {'amount': contribution.amount, 'screenshot_url': contribution.screenshot.url if contribution.screenshot else ''} for contribution in contributions}
    return JsonResponse(data)