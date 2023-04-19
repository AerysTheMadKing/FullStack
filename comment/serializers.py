from rest_framework import serializers

from comment.models import Comments


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Comments
        fields = '__all__'


