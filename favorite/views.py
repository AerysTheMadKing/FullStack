from rest_framework import generics, permissions
from favorite import serializers


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)










