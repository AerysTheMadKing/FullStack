from django.db import models

from account.models import CustomUser
from category.models import Category


class Product(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.CharField(max_length=150)
    director = models.CharField(max_length=160)
    year = models.DateField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

