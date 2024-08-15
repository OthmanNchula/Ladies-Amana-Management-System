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
    path('manage-user/<int:user_id>/mchango/', views.manage_mchango, name='manage_mchango'),
    path('manage-user/<int:user_id>/mchango/save/', views.save_mchango, name='save_mchango'),
    path('manage-user/<int:user_id>/swadaqa/', views.manage_swadaqa, name='manage_swadaqa'),
    path('manage-user/<int:user_id>/swadaqa/data/<int:year>/', views.swadaqa_data, name='swadaqa_data'),
    path('manage-user/<int:user_id>/mkopo/', views.manage_mkopo, name='manage_mkopo'),
    path('manage-user/<int:user_id>/mkopo/process-request/', views.process_loan_request, name='process_loan_request'),
    path('manage-user/<int:user_id>/mkopo/payments/', views.loan_payments_view, name='loan_payments'),


   
    
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
