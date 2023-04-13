from django.db import models
from account.models import CustomUser
from product.models import Product


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.product}'

    class Meta:
        unique_together = ('owner', 'product')