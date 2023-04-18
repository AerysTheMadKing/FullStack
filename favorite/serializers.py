
from rest_framework import serializers
from favorite.models import Favorites


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favorites
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.favorites.filter(product=product).exists():
            favorite = user.favorites.filter(product=product)
            favorite.delete()
            raise serializers.ValidationError('Deleted from favorites!')
        return attrs

