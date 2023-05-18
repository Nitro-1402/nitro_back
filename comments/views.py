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
from .permissions import *

class CommentViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type_id', 'object_id', 'profile']
    permission_classes = [CommentPermission]
    authentication_classes = [JWTAuthentication]
    queryset = Comment.objects.select_related('profile').select_related('parent_comment').select_related('content_type').all()
    serializer_class = CommentSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class LikeCommentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_id', 'profile_id']
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer


    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class DeleteLikeView(APIView):
    def delete(self, request):
        comment_id = request.GET.get('comment_id')
        profile_id = request.GET.get('profile_id')
        follow = get_object_or_404(LikeComment, comment_id=comment_id, profile_id=profile_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LikedCommentsView(APIView):
    def get(self, request):
        profile_id = request.GET.get('profile_id')
        queryset = LikeComment.objects.filter(user_id = profile_id)
        serializer = LikedCommentsSerializer(queryset, many=True)
        return Response(serializer.data)
