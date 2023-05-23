from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Q
from .models import MenuItem, OrderModel, Location, OrderItem
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from blog.views import PostListView
from .forms import AdForm, AdImageFormSet, CommentForm
from .models import Ad, AdImage, Comment
from django.db.models import Count
from django.db.models.functions import Coalesce


def ad_list(request):
    query = request.GET.get('q')

    if query:
        ads = Ad.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-id')
    else:
        ads = Ad.objects.all().annotate(like_count=Count('likes')).order_by('-like_count', '-id')

    categories = dict(Ad.CATEGORY_CHOICES)

    # Retrieve comments count for each ad
    ad_comments_count = Ad.objects.annotate(comment_count=Coalesce(Count('comments'), 0)).values('id', 'comment_count')

    ad_comments = {}
    for entry in ad_comments_count:
        ad_id = entry['id']
        comment_count = entry['comment_count']
        ad_comments[ad_id] = comment_count

    liked_ads = request.session.get('liked_ads', [])  # Get liked ads from session or initialize as empty list

    return render(request, 'customer/ad_list.html', {'ads': ads, 'categories': categories, 'ad_comments': ad_comments, 'liked_ads': liked_ads})


def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        formset = AdImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            ad = form.save()
            for image_form in formset:
                image = image_form.cleaned_data.get('image')
                if image:
                    AdImage.objects.create(ad=ad, image=image)

            return redirect('customer:ad-list')

    else:
        form = AdForm()
        formset = AdImageFormSet()

    comment_form = CommentForm()  # Create an instance of the CommentForm

    context = {'form': form, 'formset': formset, 'comment_form': comment_form}
    return render(request, 'customer/create_ad.html', context)


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    comments = ad.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            comment = Comment(ad=ad, content=content)
            comment.save()
            return redirect('customer:ad-detail', ad_id=ad_id)
    else:
        comment_form = CommentForm()

    return render(request, 'customer/ad_detail.html', {'ad': ad, 'comments': comments, 'comment_form': comment_form})

def add_comment(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.save()
            return redirect('customer:ad-detail', ad_id=ad_id)
    else:
        form = CommentForm()

    return render(request, 'customer/add_comment.html', {'form': form})


class Index(PostListView):
    template_name = 'customer/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')



class Order(View):
    def get(self, request, *args, **kwargs):
        # Get items that are available and verified
        items = MenuItem.objects.filter(Q(availability=True) | Q(is_verified=True)).order_by('-id')

        # Get all locations and users
        locations = Location.objects.all()
        users = User.objects.all()

        context = {
            'items': items,
            'locations': locations,
            'users': users,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        specifics = request.POST.get('specifics')
        email = request.POST.get('email')
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
            specifics=specifics,
            email=email,
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

        total_price = order.price + order.location.delivery_fee
        context = {
            'pk': order.pk,
            'order_items': order.order_items.all(),
            'price': order.price,
            'location': order.location,
            'delivery_fee': order.location.delivery_fee,
            'total_price': total_price,
        }

        return render(request, 'customer/order_confirmation.html', context)


def get_invoice(request, pk):
    order = OrderModel.objects.get(pk=pk)
    items = order.order_items.all()
    price = sum(item.item.price * item.quantity for item in items)
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
                                                   'name': name,'specifics': specifics, 'email': email, 'street': street,
                                                   'city': city, 'order': order})

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
        items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(category__name__icontains=query) # use name__icontains on the related Category model
        )
        locations = Location.objects.all()

        context = {
            'items': items,
            'locations': locations,
        }

        return render(request, 'customer/order.html', context)
