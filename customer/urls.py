from django.urls import path
from .views import Index, About, Order, OrderConfirmation,Menu, MenuSearch
from customer import views

app_name = 'customer'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>/', OrderConfirmation.as_view(), name='order-confirmation'),
    path('order/<int:pk>/invoice/', views.get_invoice, name='invoice'),
]