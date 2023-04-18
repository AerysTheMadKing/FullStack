from rest_framework import generics, permissions
from rest_framework.response import Response

from like.models import Like
from like.serializers import LikeSerializer
from product.models import Product
from product.permissions import IsAuthor


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