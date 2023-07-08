from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Location, Ad, AdImage, Event

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

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'name', 'email', 'is_shipped', 'total_price')
    list_filter = ('is_shipped',)
    search_fields = ('name', 'email')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Event)
