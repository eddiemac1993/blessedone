from django.urls import path
from .views import menu_dashboard, delete_item,  update_item

app_name = 'deliver'
urlpatterns = [
    path('dashboard/', menu_dashboard, name='menu_dashboard'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('update_item/<int:item_id>/', update_item, name='update_item'),
]
