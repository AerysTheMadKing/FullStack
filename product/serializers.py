from django.db.models import Avg
from rest_framework import serializers

from comment.serializers import CommentSerializer
from like.serializers import LikeSerializer
from .models import Product

class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    @staticmethod
    def is_favorite(product, user):
        return user.favorites.filter(product=product).exists()
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))
        repr['comments count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        rating = repr['rating']
        rating['rating__count'] = instance.ratings.count()
        repr['likes_count'] = instance.likes.count()
        repr['liked_users'] = LikeSerializer(instance=instance.likes.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_favorite'] = self.is_favorite(instance, user)
        return repr

    class Meta:
        model = Product
        fields = '__all__'



class ProductDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    rating = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    liked_users = LikeSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    # year = serializers.

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def is_favorite(product, user):
        return user.favorites.filter(product=product).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))
        repr['comments count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        rating = repr['rating']
        rating['rating__count'] = instance.ratings.count()
        repr['likes_count'] = instance.likes.count()
        repr['liked_users'] = LikeSerializer(instance=instance.likes.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_favorite'] = self.is_favorite(instance, user)
        return repr


