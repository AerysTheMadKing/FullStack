from django.db.models import Avg
from rest_framework import serializers

from comment.serializers import CommentSerializer
from .models import Product

class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))
        repr['comments count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        rating = repr['rating']
        rating['rating__count'] = instance.ratings.count()
        return repr

    class Meta:
        model = Product
        fields = '__all__'



    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['comments count'] = instance.comments.count()
    #     repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
    #
    #     return repr

class ProductDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))
        repr['comments count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        rating = repr['rating']
        rating['rating__count'] = instance.ratings.count()
        return repr
