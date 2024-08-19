from django.urls import path
from . import views

app_name = 'michango_App'

urlpatterns = [
    path('', views.mchango_view, name='mchango'),
    path('data/<int:year>/', views.mchango_data, name='mchango_data'),
]
