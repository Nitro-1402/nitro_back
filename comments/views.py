from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user').select_related('parent_comment').select_related('content_type').all()
    serializer_class = CommentSerializer

class LikeCommentViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_id', 'user_id']
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer

    # def delete(self, request):
    #     comment_id = request.GET.get('comment_id')
    #     user_id = request.GET.get('user_id')
    #     follow = get_object_or_404(LikeComment, comment_id=comment_id, user_id=user_id)
    #     follow.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)