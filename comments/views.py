from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class CommentViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type_id', 'object_id', 'user']
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Comment.objects.select_related('user').select_related('parent_comment').select_related('content_type').all()
    serializer_class = CommentSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
        else:
            return super().get_authenticators()

class LikeCommentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_id', 'user_id']
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer

class DeleteLikeView(APIView):
    def delete(self, request):
        comment_id = request.GET.get('comment_id')
        user_id = request.GET.get('user_id')
        follow = get_object_or_404(LikeComment, comment_id=comment_id, user_id=user_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LikedCommentsView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        queryset = LikeComment.objects.filter(user_id = user_id)
        serializer = LikedCommentsSerializer(queryset, many=True)
        return Response(serializer.data)
