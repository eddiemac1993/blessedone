from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ['employee', 'date']

class Leave(models.Model):
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal Leave'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_date = models.DateField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField()

from django.db import models
from django.contrib.auth.models import User

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.overtime_pay - self.deductions
        super().save(*args, **kwargs)

class JobOpening(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField()

class Applicant(models.Model):
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='under_review')

class Training(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    trainer = models.CharField(max_length=100)

class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='enrolled')