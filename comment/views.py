from django.shortcuts import render
from rest_framework.response import Response

from product.permissions import IsAuthorOrAdmin
from . models import Comments
from rest_framework import generics, permissions, status
from . import serializers
# Create your views here.


class CommentCreateView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.DestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = IsAuthorOrAdmin,

    # def delete(self, request, *args, **kwargs):
    #     comment_id = self.kwargs['comments_id']
    #     comment = Comments.objects.get(id=comment_id).delete()
    #     return Response(f'Comment with {comment_id} id is deleted', status=status.HTTP_204_NO_CONTENT)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response('Comment deleted', status=status.HTTP_204_NO_CONTENT)