from rest_framework import generics, permissions
from apps.favorite import serializers
from apps.favorite.models import Favorites
from apps.product.permissions import IsAuthor




class FavoriteCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsAuthor)
    serializer_class = serializers.FavoriteSerializer


    def get_queryset(self):
        my_favorites = Favorites.objects.filter(user=self.request.user)
        return my_favorites

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorites.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

