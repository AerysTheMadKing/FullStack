from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.likes.filter(product=product).exists():
            raise serializers.ValidationError('You already liked this post!')
        return attrs