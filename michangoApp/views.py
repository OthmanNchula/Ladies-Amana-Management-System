# michangoApp/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Michango
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='/account/login/')
def michango_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Fetch contributions for the user
    contributions = Michango.objects.filter(user=request.user)
    data_by_year = {}
    for year in years:
        yearly_contributions = contributions.filter(year=year)
        data_by_year[year] = {contribution.month: contribution.amount for contribution in yearly_contributions}

    return render(request, 'michangoApp/michango.html', {
        'current_year': current_year,
        'years': years,
        'data_by_year': data_by_year,
        'months': month_names
    })
    


@login_required(login_url='/account/login/')
def michango_data(request, year):
    contributions = Michango.objects.filter(user=request.user, year=year)
    data = {contribution.month: contribution.amount for contribution in contributions}
    return JsonResponse(data)

