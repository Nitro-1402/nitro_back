from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import mixins
from rest_framework.permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from .permissions import *


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        try:
            profile_id = user.profile.id
        except:
            profile_id = 0
        return Response({
            'id': user.id,
            'profile_id' : profile_id,
            'email': str(user.email),
            'username': str(user.username),
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

class ProfileViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = EditProfileSerializer
    permission_classes = [ProfilePermission]

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class FollowersListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followers').all()
    serializer_class = FollowersSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class FollowingsListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followings').all()
    serializer_class = FollowingsSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class AddFollowViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = UserFollow.objects.select_related('follower_id').select_related('following_id').all()
    serializer_class = AddFollowSerializer
    permission_classes = [AddFollowPermission]

class DeleteFollowView(APIView):
    def delete(self, request):
        follower_id = request.GET.get('follower_id')
        following_id = request.GET.get('following_id')
        follow = get_object_or_404(UserFollow, follower_id=follower_id, following_id=following_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PostViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile']

    queryset = Post.objects.filter(is_premium = False).select_related('profile')
    serializer_class = PostSerializer

class PremiumPostViewSet(ModelViewSet):
    permission_classes = [IsSubscriber] 
    serializer_class = PremiumPostSerializer

    def get_queryset(self):
        return Post.objects.filter(profile_id=self.kwargs['profile_pk']).filter(is_premium=True)
    
    def get_serializer_context(self): 
        return {'profile_id': self.kwargs['profile_pk']}

class SubscribersViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('subscribers__subscriber_id__user').all()
    serializer_class = SubscribersSerializer

class AddSubscriberViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Subscribe.objects.select_related('profile_id').select_related('subscriber_id').all()
    serializer_class = AddSubscriberSerializer

class DeleteSubscribeView(APIView):
    def delete(self, request):
        user_id = request.GET.get('user_id')
        subscriber_id = request.GET.get('subscriber_id')
        subscribe = get_object_or_404(Subscribe, user_id=user_id, subscriber_id=subscriber_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
