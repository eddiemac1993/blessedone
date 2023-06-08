from django.urls import path
from . import views

app_name = 'pdf_manager'

urlpatterns = [
    path('pdf-list/', views.pdf_list_view, name='pdf_list'),
    path('upload/', views.pdf_upload, name='pdf_upload'),
    # Other URL patterns for your app...
]
