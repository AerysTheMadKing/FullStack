from rest_framework import generics, permissions
from category.models import Category
from . import serializers


class CategoryCreateListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return permissions.IsAdminUser(),

        return permissions.AllowAny(),


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),

        return permissions.IsAdminUser(),
