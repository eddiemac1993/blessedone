from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Expense(models.Model):
    COMPANY_CHOICES = [
        ('SC', 'SC'),
        ('CMM', 'CMM'),
    ]
    date = models.DateField()
    company = models.CharField(max_length=3, choices=COMPANY_CHOICES)
    reason = models.TextField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.date} - {self.company} - K{self.amount}"

