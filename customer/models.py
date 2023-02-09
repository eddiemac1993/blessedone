from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('category', related_name='item')
    availability = models.BooleanField(default=True)

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

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(default="example@email.com")
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='order', null=True, blank=True)
    is_shipped = models.BooleanField(default=False)

    def total_price(self):
        total = self.price
        if self.location:
            total += self.location.delivery_fee
        return total


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
