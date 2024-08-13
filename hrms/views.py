from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, Attendance, Leave, Performance
from .forms import EmployeeForm, AttendanceForm, LeaveForm, PerformanceForm

def dashboard(request):
    employees = Employee.objects.all()
    return render(request, 'hrms/dashboard.html', {'employees': employees})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hrms/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'hrms/employee_detail.html', {'employee': employee})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'hrms/employee_form.html', {'form': form})

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'hrms/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'hrms/attendance_form.html', {'form': form})

@login_required
def leave_list(request):
    leaves = Leave.objects.all()
    return render(request, 'hrms/leave_list.html', {'leaves': leaves})

@login_required
def leave_create(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
    return render(request, 'hrms/leave_form.html', {'form': form})

@login_required
def performance_list(request):
    performances = Performance.objects.all()
    return render(request, 'hrms/performance_list.html', {'performances': performances})

@login_required
def performance_create(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_list')
    else:
        form = PerformanceForm()
    return render(request, 'hrms/performance_form.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payroll, JobOpening, Applicant, Training, EmployeeTraining
from .forms import PayrollForm, JobOpeningForm, ApplicantForm, TrainingForm, EmployeeTrainingForm
from django.db.models import Sum, Avg
from django.http import HttpResponse
import csv

# ... (previous views)

@login_required
def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'hrms/payroll_list.html', {'payrolls': payrolls})

@login_required
def payroll_create(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'hrms/payroll_form.html', {'form': form})

@login_required
def job_opening_list(request):
    job_openings = JobOpening.objects.all()
    return render(request, 'hrms/job_opening_list.html', {'job_openings': job_openings})

@login_required
def job_opening_create(request):
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_opening_list')
    else:
        form = JobOpeningForm()
    return render(request, 'hrms/job_opening_form.html', {'form': form})

@login_required
def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'hrms/applicant_list.html', {'applicants': applicants})

@login_required
def applicant_create(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm()
    return render(request, 'hrms/applicant_form.html', {'form': form})

@login_required
def training_list(request):
    trainings = Training.objects.all()
    return render(request, 'hrms/training_list.html', {'trainings': trainings})

@login_required
def training_create(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'hrms/training_form.html', {'form': form})

@login_required
def employee_training_list(request):
    employee_trainings = EmployeeTraining.objects.all()
    return render(request, 'hrms/employee_training_list.html', {'employee_trainings': employee_trainings})

@login_required
def employee_training_create(request):
    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_training_list')
    else:
        form = EmployeeTrainingForm()
    return render(request, 'hrms/employee_training_form.html', {'form': form})

@login_required
def generate_payroll_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payroll_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Pay Period', 'Basic Salary', 'Overtime Pay', 'Deductions', 'Net Salary'])

    payrolls = Payroll.objects.all()
    for payroll in payrolls:
        writer.writerow([payroll.employee, payroll.pay_period, payroll.basic_salary, payroll.overtime_pay, payroll.deductions, payroll.net_salary])

    return response

@login_required
def hr_dashboard(request):
    total_employees = Employee.objects.count()
    avg_salary = Payroll.objects.aggregate(Avg('basic_salary'))['basic_salary__avg']
    open_positions = JobOpening.objects.filter(closing_date__gte=timezone.now()).count()
    upcoming_trainings = Training.objects.filter(start_date__gte=timezone.now()).count()

    context = {
        'total_employees': total_employees,
        'avg_salary': avg_salary,
        'open_positions': open_positions,
        'upcoming_trainings': upcoming_trainings,
    }
    return render(request, 'hrms/hr_dashboard.html', context)