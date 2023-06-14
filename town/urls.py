from django.urls import path
from . import views

app_name = 'town'

urlpatterns = [
    path('places/', views.place_list, name='place_list'),
    path('rooms/', views.room_list, name='room_list'),
    path('adventures/', views.adventure_list, name='adventure_list'),
    path('adventure/<int:adventure_id>/booking/', views.adventure_booking, name='adventure_booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('agriculture/', views.agriculture_view, name='agriculture'),
    path('autospare/', views.autospare_view, name='autospare'),
    path('electronics/', views.electronics_view, name='electronics'),
]