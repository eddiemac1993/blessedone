from django.contrib import admin
from .models import Place, Hotel, TouristCompany, Adventure, Booking

admin.site.register(Place)
admin.site.register(Hotel)
admin.site.register(TouristCompany)
admin.site.register(Adventure)
admin.site.register(Booking)
