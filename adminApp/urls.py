from django.urls import path
from . import views

app_name = 'admin_App'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('superuser-login/', views.superuser_login_view, name='superuser_login'),
    
    #members
    path('members/', views.members, name='members'),
    path('manage-user/<int:user_id>/', views.manage_user, name='manage_user'),
    path('manage-user/<int:user_id>/mtaji/', views.manage_mtaji, name='manage_mtaji'),
    path('manage-user/<int:user_id>/mtaji/data/<int:year>/', views.mtaji_data, name='mtaji_data'),
   
    
    #loans
    path('loan-requests/', views.loan_requests, name='loan_requests'),
    path('members-loans/', views.members_loans, name='members_loans'),
    path('approved-loans/', views.approved_loans, name='approved_loans'),
    path('rejected-loans/', views.rejected_loans, name='rejected_loans'),
    path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('reject-loan/<int:loan_id>/', views.reject_loan, name='reject_loan'),
    path('approved-loans/', views.approved_loans, name='approved_loans'),
    path('rejected-loans/', views.rejected_loans, name='rejected_loans'),
    
    #mtaji
    path('mitaji/', views.mitaji_view, name='mitaji'), 
    
    #mchango
    path('michango/', views.michango_view, name='michango'),
    
    # verification urls
    path('verification/', views.verification, name='verification'),
    path('approve-change/<int:change_id>/', views.approve_change, name='approve_change'),
    path('reject-change/<int:change_id>/', views.reject_change, name='reject_change'),
    path('verified-actions/', views.verified_actions, name='verified_actions'),
    
    # mengineyo urls
    path('mengineyo/', views.mengineyo, name='mengineyo'),
    
]
