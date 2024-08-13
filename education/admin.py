# education/admin.py

from django.contrib import admin
from .models import PDFResource, BlogPost, FreeTrial, SuccessStory

admin.site.register(PDFResource)
admin.site.register(BlogPost)
admin.site.register(FreeTrial)
admin.site.register(SuccessStory)
