from django.db import models
from account.models import CustomUser
from product.models import Product


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
