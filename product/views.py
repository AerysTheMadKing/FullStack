from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action

from comment.serializers import CommentSerializer
from rating.serializers import RatingSerializer
from .models import Product
from .import serializers
from .permissions import IsAuthor


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return permissions.IsAdminUser(),
        return [permissions.IsAuthenticatedOrReadOnly()]

    # /api/v1/products/<id>/reviews/
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'GET':
            rating = product.ratings.all()
            serializer = RatingSerializer(instance=rating, many=True).data
            return response.Response(serializer, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return response.Response('You already rated this product', status=400)

            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return response.Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return response.Response('You did\'t rated this product', status=400)

            rating = product.ratings.get(owner=user)
            rating.delete()
            return response.Response('Successfully deleted!', status=204)
    #
    # @action(['GET', 'POST', 'DELETE'], detail=True)
    # def comments(self, request, pk):
    #     product = self.get_object()
    #     user = request.user
    #
    #     if request.method == 'GET':
    #         comment = product.comments.all()
    #         serializer = RatingSerializer(instance=comment, many=True).data
    #         return response.Response(serializer, status=200)
    #
    #     elif request.method == 'POST':
    #         data = request.data
    #         serializer = CommentSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(owner=user, product=product)
    #         return response.Response(serializer.data, status=201)
    #
    #     else:
    #         comment = product.comments.get(owner=user)
    #         comment.delete()
    #         return response.Response('Successfully deleted!', status=204)


