from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from .models import MenuItem, OrderModel, Location, OrderItem
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.db.models.functions import Coalesce
from decimal import Decimal
import random



class Index(ListView):
    model = MenuItem
    template_name = 'customer/index.html'
    context_object_name = 'menu_items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Shuffle the queryset randomly
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset


class Ai(View):
    template_name = 'customer/ai.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        response = 'Hi, this is my response'
        return JsonResponse({'message': message, 'response': response})


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # Get items that are available and verified
        items_by_category = {}

        # Group items by category
        for item in MenuItem.objects.filter(Q(availability=True) | Q(is_verified=True)).order_by('?'):
            for category in item.category.all():
                if category not in items_by_category:
                    items_by_category[category] = []
                items_by_category[category].append(item)

        # Get all locations and users
        locations = Location.objects.all()
        users = User.objects.all()

        context = {
            'items_by_category': items_by_category,
            'locations': locations,
            'users': users,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        street = request.POST.get('street')
        phone_number = request.POST.get('phone_number')
        location_id = request.POST.get('location')
        agent_id = request.POST.get('agent')
        agent = User.objects.get(pk=agent_id)
        location = Location.objects.get(pk=location_id)
        order_items = []

        items = request.POST.getlist('items[]')
        quantities = request.POST.getlist('quantities[]')

        for item, quantity in zip(items, quantities):
            menu_item = MenuItem.objects.get(pk=int(item))
            order_item = OrderItem.objects.create(
                item=menu_item,
                quantity=int(quantity)
            )
            order_items.append(order_item)

        price = sum([item.item.price * item.quantity for item in order_items])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            street=street,
            phone_number=phone_number,
            location=location,
            agent=agent
        )
        order.order_items.add(*order_items)

        return redirect('customer:order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        # Calculate the discount amount (8% of the total price)
        discount_percentage = Decimal('0.08')  # Use Decimal for precise arithmetic
        discount_amount = discount_percentage * order.price

        total_price = order.price + order.location.delivery_fee + discount_amount

        context = {
            'pk': order.pk,
            'order_items': order.order_items.all(),
            'price': order.price,
            'location': order.location,
            'delivery_fee': order.location.delivery_fee,
            'total_price': total_price,
            'discount_amount': discount_amount,
        }

        return render(request, 'customer/order_confirmation.html', context)


def get_invoice(request, pk):
    order = OrderModel.objects.get(pk=pk)
    items = order.order_items.all()

    # Calculate the total price with discount
    discount_percentage = Decimal('0.08')  # 5% discount
    discount_amount = discount_percentage * order.price
    price = sum((item.item.price * item.quantity for item in items))
    total_price = price + order.location.delivery_fee + discount_amount

    # Get the customer details from the order object
    name = order.name
    street = order.street
    city = order.city

    # Render the HTML template to be converted to PDF
    html = render_to_string('customer/invoice.html', {'items': items, 'pk': pk, 'price': price,
                                                      'delivery_fee': order.location.delivery_fee,
                                                      'total_price': total_price,
                                                      'discount_amount': discount_amount,
                                                      'name': name,
                                                      'street': street, 'city': city, 'order': order})

    # Convert the HTML to PDF and return it as response
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        menu_items = list(menu_items)
        random.shuffle(menu_items)

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        # Shuffle the menu items randomly
        menu_items = list(menu_items)
        random.shuffle(menu_items)

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class OrderSearch(MenuSearch):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(category__name__icontains=query) # use name__icontains on the related Category model
        )

        # Get all locations and users
        locations = Location.objects.all()
        users = User.objects.all()

        context = {
            'items': items,
            'locations': locations,
            'users': users,
            'searched_item': query,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        street = request.POST.get('street')
        phone_number = request.POST.get('phone_number')
        location_id = request.POST.get('location')
        agent_id = request.POST.get('agent')
        agent = User.objects.get(pk=agent_id)
        location = Location.objects.get(pk=location_id)
        order_items = []

        items = request.POST.getlist('items[]')
        quantities = request.POST.getlist('quantities[]')

        for item, quantity in zip(items, quantities):
            menu_item = MenuItem.objects.get(pk=int(item))
            order_item = OrderItem.objects.create(
                item=menu_item,
                quantity=int(quantity)
            )
            order_items.append(order_item)

        price = sum([item.item.price * item.quantity for item in order_items])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            street=street,
            phone_number=phone_number,
            location=location,
            agent=agent
        )
        order.order_items.add(*order_items)

        return redirect('customer:order-confirmation', pk=order.pk)
