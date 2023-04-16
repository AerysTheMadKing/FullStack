from rest_framework import serializers

from comment.models import Comments


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comments
        fields = '__all__'


