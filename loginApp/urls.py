from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


app_name = 'login_App'

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_App:login'), name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-info/', views.edit_info, name='edit_info'),
    path('upload-payment-image/', views.upload_payment_image, name='upload_payment_image'),
    path('payment-images/', views.payment_images, name='payment_images'),
    path('payment-images/delete/<int:image_id>/', views.delete_payment_image, name='delete_payment_image'),
    
    path('change-password-prompt/', views.change_password_prompt, name='change_password_prompt'),
    
    # Password reset URLs
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='loginApp/password_reset.html',
        email_template_name='loginApp/password_reset_email.html',
        subject_template_name='loginApp/password_reset_subject.txt',
        success_url=reverse_lazy('login_App:password_reset_done')  # Corrected URL using reverse_lazy
    ), name='reset_password'),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="loginApp/password_reset_sent.html"
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="loginApp/password_reset_complete.html"
    ), name='password_reset_complete'),
    
]

