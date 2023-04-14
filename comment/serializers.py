from rest_framework import serializers

from comment.models import Comments


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comments
        fields = '__all__'
