from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, OrderModel, Location
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Game(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/game.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        items = MenuItem.objects.filter(availability=True)
        locations = Location.objects.all()

        context = {
            'items': items,
            'locations': locations,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        specifics = request.POST.get('specifics')
        email = request.POST.get('email')
        street = request.POST.get('street')
        phone_number = request.POST.get('phone_number')
        location_id = request.POST.get('location')

        location = Location.objects.get(pk=location_id)

        order_items = {
            'item': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }

            order_items['item'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['item']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            specifics=specifics,
            email=email,
            street=street,
            phone_number=phone_number,
            location=location
            )
        order.items.add(*item_ids)

        return redirect('customer:order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        total_price = order.price + order.location.delivery_fee
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
            'location': order.location,
            'delivery_fee': order.location.delivery_fee,
            'total_price': total_price,
        }

        return render(request, 'customer/order_confirmation.html', context)


def get_invoice(request, pk):
    order = OrderModel.objects.get(pk=pk)
    items = order.items.all()
    price = sum(item.price for item in items)
    delivery_fee = order.total_price() - order.price
    total = price + delivery_fee

    # Get the customer details from the order object
    name = order.name
    specifics = order.specifics
    email = order.email
    street = order.street
    city = order.city

    # Render the HTML template to be converted to PDF
    html = render_to_string('customer/invoice.html', {'items': items, 'pk': pk, 'price': price,
                                                       'delivery_fee': delivery_fee, 'total_price': total,
                                                       'name': name, 'specifics': specifics, 'email': email, 'street': street,
                                                       'city': city })

    # Convert the HTML to PDF and return it as response
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response



class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

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

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class OrderSearch(MenuSearch):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        items = MenuItem.objects.filter(Q(name__icontains=query) | Q(price__icontains=query))
        locations = Location.objects.all()

        context = {
            'items': items,
            'locations': locations,
        }

        return render(request, 'customer/order.html', context)
