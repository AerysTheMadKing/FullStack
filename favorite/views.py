from rest_framework import generics, permissions
from favorite import serializers
from favorite.models import Favorites
from product.permissions import IsAuthor




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

