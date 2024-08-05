# michangoApp/urls.py
from django.urls import path
from . import views

app_name = 'michango_App'

urlpatterns = [
    path('', views.michango_view, name='michango'),
    path('<int:year>/', views.michango_view, name='michango'),
]
