from django.urls import path
from .views import menu_dashboard, delete_item,  update_item, menu_dashboardx

app_name = 'deliver'
urlpatterns = [
    path('dashboard/', menu_dashboard, name='menu_dashboard'),
    path('dashboardx/', menu_dashboardx, name='menu_dashboardx'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('update_item/<int:item_id>/', update_item, name='update_item'),
]
