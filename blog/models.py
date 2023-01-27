from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(default="default.jpg", upload_to='images/')
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField(default="")

    def __str__(self):
        return self.user.username


