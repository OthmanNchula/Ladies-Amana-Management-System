from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum  # Add this import
from .models import Michango
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='/account/login/')
def mchango_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Fetch contributions for the user
    contributions = Michango.objects.filter(user=request.user)

    # Calculate total mchango for the current year
    total_mchango_year = contributions.filter(year=current_year).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate total mchango for all years
    total_mchango_all_years = contributions.aggregate(total=Sum('amount'))['total'] or 0

    data_by_year = {}
    for year in years:
        yearly_contributions = contributions.filter(year=year)
        if yearly_contributions.exists():
            data_by_year[year] = {contribution.month: contribution.amount for contribution in yearly_contributions}
        else:
            data_by_year[year] = {i + 1: 0 for i in range(12)}

    return render(request, 'michangoApp/mchango.html', {
        'current_year': current_year,
        'years': years,
        'data_by_year': data_by_year,
        'months': month_names,
        'total_mchango_year': total_mchango_year,
        'total_mchango_all_years': total_mchango_all_years,
    })

@login_required(login_url='/account/login/')
def mchango_data(request, year):
    contributions = Michango.objects.filter(user=request.user, year=year)
    data = {contribution.month: contribution.amount for contribution in contributions}
    return JsonResponse(data)
