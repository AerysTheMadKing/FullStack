from datetime import date

from django.db import models

from account.models import CustomUser


class Product(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=200)
    country = models.CharField(max_length=150)
    director = models.CharField(max_length=160)
    year = models.DateField()
    image = models.ImageField(upload_to='images/')
    film = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title