from django.db import models

from apps.account.models import CustomUser
from apps.product.models import Product


# Create your models here.
class Comments(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} -> {self.product}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
