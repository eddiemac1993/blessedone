from django import forms
from .models import Employee, Attendance, Leave, Performance

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'department', 'position', 'hire_date']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'is_present']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date']

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['employee', 'review_date', 'rating', 'comments']
        
        
from django import forms
from .models import Payroll, JobOpening, Applicant, Training, EmployeeTraining

# ... (previous forms)

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'pay_period', 'basic_salary', 'overtime_pay', 'deductions']

class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['title', 'department', 'description', 'requirements', 'closing_date']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job_opening', 'name', 'email', 'resume']

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'description', 'start_date', 'end_date', 'trainer']

class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = EmployeeTraining
        fields = ['employee', 'training', 'completion_date', 'status']