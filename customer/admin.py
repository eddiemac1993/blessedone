from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Location, Ad, AdImage

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone_number', 'location', 'price', 'category', 'created_at')
    search_fields = ('title', 'phone_number', 'location')
    list_filter = ('category',)
    list_per_page = 20

@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'image')
    list_filter = ('ad',)
    
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Location)