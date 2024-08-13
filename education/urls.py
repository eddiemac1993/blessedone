# education/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('free-trial/', views.free_trial, name='free_trial'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('pdfs/<str:filename>/', views.view_pdf, name='view_pdf'),
    path('pdfs/<path:filename>/', views.view_pdf, name='view_pdf'),
]
