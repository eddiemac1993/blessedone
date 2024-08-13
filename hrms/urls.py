from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/create/', views.leave_create, name='leave_create'),
    path('performance/', views.performance_list, name='performance_list'),
    path('performance/create/', views.performance_create, name='performance_create'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/create/', views.payroll_create, name='payroll_create'),
    path('job-openings/', views.job_opening_list, name='job_opening_list'),
    path('job-openings/create/', views.job_opening_create, name='job_opening_create'),
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('applicants/create/', views.applicant_create, name='applicant_create'),
    path('trainings/', views.training_list, name='training_list'),
    path('trainings/create/', views.training_create, name='training_create'),
    path('employee-trainings/', views.employee_training_list, name='employee_training_list'),
    path('employee-trainings/create/', views.employee_training_create, name='employee_training_create'),
    path('reports/payroll/', views.generate_payroll_report, name='generate_payroll_report'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
]