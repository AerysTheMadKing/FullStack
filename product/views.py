from django.db.models import Avg, Count
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from comment.serializers import CommentSerializer
from rating.serializers import RatingSerializer
from .models import Product
from . import serializers
from .permissions import IsAuthor


class StandartResultPagination(PageNumberPagination):
    page_size = 16
    page_query_param = 'page'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.annotate(
            rating=Avg("ratings__rating"),
            comment_count=Count("comments__id"),
        ).prefetch_related("owner", "comments")

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
                return response.Response('You have already rated this post', status=400)
            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return response.Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return response.Response('You did\'t rated this post', status=400)

            rating = product.ratings.get(owner=user)
            rating.delete()
            return response.Response('Successfully deleted!', status=204)
