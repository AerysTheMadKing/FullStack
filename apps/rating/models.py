from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product
from django.core.cache import cache

User = get_user_model()


from django.core.cache import cache

class Rating(models.Model):
    RATING_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def cache_key(self):
        return f"rating_{self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(self.cache_key(), self)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(self.cache_key())

    @classmethod
    def get_rating(cls, rating_id):
        cache_key = f"rating_{rating_id}"
        rating = cache.get(cache_key)
        if not rating:
            rating = cls.objects.select_related('product', 'owner').get(id=rating_id)
            cache.set(cache_key, rating)
        return rating
