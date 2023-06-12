from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields for Place model

    def __str__(self):
        return self.name

class Hotel(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    # Other fields for Hotel model

    def __str__(self):
        return self.place.name

class TouristCompany(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logos')
    website = models.URLField()
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    # Other fields for TouristCompany model

    def __str__(self):
        return self.place.name

class Adventure(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    # Other fields for Adventure model

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    num_people = models.PositiveIntegerField()
    # Other fields for Booking model

    def __str__(self):
        return f"{self.user.username}'s Booking"
