from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Michango
from datetime import datetime
from django.http import JsonResponse

@login_required(login_url='/account/login/')
def mchango_view(request):
    current_year = datetime.now().year
    years = list(range(2018, current_year + 1))
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    selected_year = int(request.GET.get('year', current_year))

    # Fetch contributions for the logged-in user
    contributions = Michango.objects.filter(user=request.user)

    # Calculate total mchango for the selected year
    total_mchango_year = contributions.filter(year=selected_year).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate total mchango for all years
    total_mchango_all_years = contributions.aggregate(total=Sum('amount'))['total'] or 0

    # Fetch michango data for each month in the selected year
    michango_by_month = [contributions.filter(year=selected_year, month=i+1).aggregate(Sum('amount'))['amount__sum'] or 0 for i in range(12)]

    # Zip months with their respective contributions
    months_and_contributions = zip(month_names, michango_by_month)

    context = {
        'current_year': current_year,
        'years': years,
        'selected_year': selected_year,
        'total_mchango_year': total_mchango_year,
        'total_mchango_all_years': total_mchango_all_years,
        'months_and_contributions': months_and_contributions,
    }

    return render(request, 'michangoApp/mchango.html', context)

@login_required(login_url='/account/login/')
def mchango_data(request, year):
    contributions = Michango.objects.filter(user=request.user, year=year)
    data = {contribution.month: contribution.amount for contribution in contributions}
    return JsonResponse(data)
