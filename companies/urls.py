from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('<int:company_id>/', views.company, name='company'),
    path('HR_dashboard/', views.HR_dashboard, name='HR_dashboard'),
    path('company_edit_info/', views.company_edit_info, name='company_edit_info'),
    path('job_post/', views.job_post, name='job_post'),
    path('view_candidate/<int:listing_id>', views.view_candidate, name='view_candidate'),
    path('toggle_job_status/<int:listing_id>/', views.toggle_job_status, name='toggle_job_status'),
]