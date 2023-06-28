from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    sponsored = models.BooleanField(default=False)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    link = models.URLField(default='https://blessedtouchs.pythonanywhere.com/ad-list/')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')
            img.thumbnail((400, 400))  # Resize the image to a maximum width/height of 800 pixels
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=70)  # Save the image as JPEG with 70% quality
            self.image = SimpleUploadedFile(self.image.name, img_io.getvalue(), content_type='image/jpeg')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ad(models.Model):
    CATEGORY_CHOICES = (
        ('item', 'Items'),
        ('agriculture', 'Agriculture'),
        ('hardware', 'Hardware'),
        ('food', 'Food'),
        ('job', 'Jobs'),
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('books', 'Books'),
        ('health', 'Health'),
        ('beauty', 'Beauty'),
        ('sports', 'Sports'),
        ('toys', 'Toys'),
        ('automotive', 'Automotive'),
        ('music', 'Music'),
        ('art', 'Art'),
        ('collectibles', 'Collectibles'),
        ('baby', 'Baby'),
        ('pet', 'Pet'),
        ('tools', 'Tools'),
        ('outdoors', 'Outdoors'),
        ('jewelry', 'Jewelry'),
        ('movies', 'Movies'),
        ('games', 'Games'),
        ('crafts', 'Crafts'),
        ('office', 'Office'),
        ('travel', 'Travel'),
        ('fitness', 'Fitness'),
        ('antiques', 'Antiques'),
        ('instruments', 'Instruments'),
        ('party', 'Party'),
        ('vintage', 'Vintage'),
        ('technology', 'Technology'),
        ('furniture', 'Furniture'),
        ('kitchen', 'Kitchen'),
        ('cosmetics', 'Cosmetics'),
        ('stationery', 'Stationery'),
        ('gifts', 'Gifts'),
        ('medical', 'Medical'),
        ('real_estate', 'Real Estate'),
        ('services', 'Services'),
        # Add more categories here
    )

    title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, default='Livingstone, Zambia')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Comment on Ad '{self.ad.title}'"


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads/')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')
            img.thumbnail((400, 400))  # Resize the image to a maximum width/height of 800 pixels
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=70)  # Save the image as JPEG with 70% quality
            self.image = SimpleUploadedFile(self.image.name, img_io.getvalue(), content_type='image/jpeg')

        super().save(*args, **kwargs)


def default_delivered_time():
    return str(timedelta(hours=2))


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    DeliveredTime = models.TextField(default=default_delivered_time)
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='items')
    availability = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)  # New field for verified items

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item.name} x {self.quantity}'


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=True)
    order_items = models.ManyToManyField(OrderItem, related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    specifics = models.EmailField(default="example@example.com")
    email = models.EmailField(default="example@example.com")
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    is_shipped = models.BooleanField(default=False)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)

    def total_price(self):
        total = self.price
        if self.location:
            total += self.location.delivery_fee
        return total

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I:%M %p")}'
