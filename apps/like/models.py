from django.db import models
from apps.account.models import CustomUser
from apps.product.models import Product


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'product')