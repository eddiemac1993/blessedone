# education/models.py

from django.db import models

class PDFResource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FreeTrial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SuccessStory(models.Model):
    student_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name
