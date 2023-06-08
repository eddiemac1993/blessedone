from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class PDFFile(models.Model):
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
