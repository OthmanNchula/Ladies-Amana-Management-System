from django.urls import path
from . import views

app_name = 'mkopo_App'

urlpatterns = [
    path('loan-request/', views.loan_request_view, name='loan_request'),
]
