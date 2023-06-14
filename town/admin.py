from django.contrib import admin
from .models import Place, Hotel, TouristCompany, Adventure, Booking, Category, ShopOwnerProfile, Post

admin.site.register(Place)
admin.site.register(Hotel)
admin.site.register(TouristCompany)
admin.site.register(Adventure)
admin.site.register(Booking)

class PostAdmin(admin.ModelAdmin):
    list_display = ['item_description', 'item_price', 'category', 'owner_profile']
    list_filter = ['category']
    search_fields = ['item_description']

class ShopOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_description']

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(ShopOwnerProfile, ShopOwnerProfileAdmin)