from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Mtaji
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='/account/login/')
def mtaji_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))

    # Fetch contributions for the user
    mtaji_list = Mtaji.objects.filter(user=request.user)
    data_by_year = {}
    for year in years:
        yearly_contributions = mtaji_list.filter(year=year)
        if yearly_contributions.exists():
            data_by_year[year] = sum(mtaji.amount for mtaji in yearly_contributions)
        else:
            data_by_year[year] = 0

    return render(request, 'mtajiApp/mtaji.html', {
        'current_year': current_year,
        'years': years,
        'data_by_year': data_by_year,
    })
    
@login_required(login_url='/account/login/')
def mtaji_data(request, year):
    contributions = Mtaji.objects.filter(user=request.user, year=year)
    total = sum(mtaji.amount for mtaji in contributions)
    data = {
        'year': year,
        'amount': total,
        'total': total
    }
    return JsonResponse(data)
