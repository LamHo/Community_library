from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    cover_image = models.ImageField(upload_to='avatars/', null = True) 

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    donator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books_donated")
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='covers/', null = True)
    file = models.FileField(upload_to='books/')



    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "donator": self.donator.username,
            "created": self.created_time,
            "last_updated": self.last_updated_time,
            "image": self.cover_image.url,          
            "file": self.file.url, 
        }

class Time_obj(models.Model):
    time = models.DateTimeField(auto_now_add=True)

