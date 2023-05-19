from django.urls import path
from .views import Index, About, Order, OrderConfirmation, Menu, MenuSearch, OrderSearch
from . import views

app_name = 'customer'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create-ad/', views.create_ad, name='create-ad'),
    path('ad-list/', views.ad_list, name='ad-list'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/search/', OrderSearch.as_view(), name='order-search'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>/', OrderConfirmation.as_view(), name='order-confirmation'),
    path('customer/order/<int:pk>/invoice/', views.get_invoice, name='invoice'),
]
