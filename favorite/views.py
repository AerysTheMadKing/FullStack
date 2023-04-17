from rest_framework import generics, permissions
from favorite import serializers
from favorite.models import Favorites
from product.permissions import IsAuthor


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorites.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

