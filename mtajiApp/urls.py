from django.urls import path
from . import views

app_name = 'mtaji_App'

urlpatterns = [
    path('', views.mtaji_view, name='mtaji'),
    path('data/<int:year>/', views.mtaji_data, name='mtaji_data'),
]
