from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from .permissions import *

class CommentViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type_id', 'object_id', 'profile']
    permission_classes = [CommentPermission]
    queryset = Comment.objects.select_related('profile').select_related('parent_comment').select_related('content_type').all()
    serializer_class = CommentSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
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
    permission_classes = [LikeCommentPermission]
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer

    @action(detail=False, methods=['DELETE'])
    def delete(self, request):
        comment_id = request.data.get('comment')
        profile_id = request.data.get('profile')

        like = get_object_or_404(LikeComment, comment_id=comment_id, profile_id=profile_id)
        like.delete()

        return Response({'message': 'like deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def profileLikes(self,request):
        profile_id = request.data.get('profile')
        queryset = LikeComment.objects.filter(profile_id = profile_id)
        serializer = LikedCommentsSerializer(queryset, many=True)
        return Response(serializer.data)


    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
                    return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()
