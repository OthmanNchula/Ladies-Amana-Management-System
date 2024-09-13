from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'login_App'

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_App:login'), name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-info/', views.edit_info, name='edit_info'),
    path('upload-payment-image/', views.upload_payment_image, name='upload_payment_image'),
    path('payment-images/', views.payment_images, name='payment_images'),
    path('payment-images/delete/<int:image_id>/', views.delete_payment_image, name='delete_payment_image'),
]
