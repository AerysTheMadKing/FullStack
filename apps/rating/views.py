from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from .models import Rating
from .serializers import RatingSerializer
from ..product.models import Product


class RatingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        product_id = request.data.get('product')
        if product_id:
            cache_key = f'product_{product_id}_ratings'
            cache.set(cache_key, None)
        return response

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product')
        if product_id:
            cache_key = 'product_{}_ratings'.format(product_id)
            ratings = cache.get(cache_key)
            print(ratings)
            if ratings is None:
                queryset = self.filter_queryset(self.get_queryset())
                ratings = queryset.filter(product_id=product_id)
                ratings = self.get_serializer(ratings, many=True).data
                cache.set(cache_key, ratings)
        else:
            ratings = self.get_queryset()
            ratings = self.get_serializer(ratings, many=True).data

        return Response(ratings)


class RatingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.get('product_{}_ratings'.format(self.get_object().product.id))
        return response
