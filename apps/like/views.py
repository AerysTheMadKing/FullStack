from django.db.models import Count
from rest_framework import generics, permissions

from apps.like.models import Like
from apps.like.serializers import LikeSerializer
from apps.product.models import Product
from apps.product.permissions import IsAuthor
from apps.product.serializers import ProductDetailSerializer


class LikeAPIView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        my_favorites = Like.objects.filter(owner=self.request.user)
        return my_favorites

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]


class RecommendationApiView(generics.ListAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        top_films = Product.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5] # need to fix
        return top_films
