from django.urls import path
from . import views

app_name = 'swadaqa_App'

urlpatterns = [
    path('', views.swadaqa_view, name='swadaqa'),
    path('data/<int:year>/', views.swadaqa_data, name='swadaqa_data'),
]
