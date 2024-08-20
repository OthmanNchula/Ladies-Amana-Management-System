from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum  # Add this import for summing contributions
from .models import Swadaqa
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='/account/login/')
def swadaqa_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))

    # Fetch contributions for the user
    swadaqa_list = Swadaqa.objects.filter(user=request.user)

    # Calculate total swadaqa for the current year
    total_swadaqa_year = swadaqa_list.filter(year=current_year).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate total swadaqa for all years
    total_swadaqa_all_years = swadaqa_list.aggregate(total=Sum('amount'))['total'] or 0

    data_by_year = {}
    for year in years:
        yearly_contributions = swadaqa_list.filter(year=year)
        data_by_year[year] = sum(swadaqa.amount for swadaqa in yearly_contributions)

    return render(request, 'swadaqaApp/swadaqa.html', {
        'current_year': current_year,
        'years': years,
        'data_by_year': data_by_year,
        'total_swadaqa_year': total_swadaqa_year,
        'total_swadaqa_all_years': total_swadaqa_all_years,
    })

@login_required(login_url='/account/login/')
def swadaqa_data(request, year):
    contributions = Swadaqa.objects.filter(user=request.user, year=year)
    total = sum(swadaqa.amount for swadaqa in contributions)
    data = {
        'year': year,
        'amount': total,
        'total': total
    }
    return JsonResponse(data)
