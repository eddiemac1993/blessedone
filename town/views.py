from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Hotel, Adventure, Post, Category
from .forms import AdventureBookingForm

def place_list(request):
    places = Place.objects.all()
    return render(request, 'town/place_list.html', {'places': places})

def room_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'town/room_list.html', {'hotels': hotels})

def adventure_list(request):
    adventures = Adventure.objects.all()
    return render(request, 'town/adventure_list.html', {'adventures': adventures})

def adventure_booking(request, adventure_id):
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    if request.method == 'POST':
        form = AdventureBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.adventure = adventure
            booking.save()
            return redirect('booking_success')
    else:
        form = AdventureBookingForm(initial={'user': request.user, 'adventure': adventure})
    return render(request, 'town/adventure_booking.html', {'form': form, 'adventure': adventure})

def booking_success(request):
    return render(request, 'town/booking_success.html')


def agriculture_view(request):
    category = get_object_or_404(Category, name='Agriculture')
    posts = Post.objects.filter(category=category)
    return render(request, 'town/agriculture.html', {'posts': posts})

def autospare_view(request):
    category = get_object_or_404(Category, name='Autospares')
    posts = Post.objects.filter(category=category)
    return render(request, 'town/autospare.html', {'posts': posts})

def electronics_view(request):
    category = get_object_or_404(Category, name='Electronics')
    posts = Post.objects.filter(category=category)
    return render(request, 'town/electronics.html', {'posts': posts})
