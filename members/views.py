from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import mixins
from rest_framework.permissions import *
from rest_framework.decorators import action
from rest_framework.parsers import *
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
    parser_classes = [FormParser,MultiPartParser]

    def get_serializer_context(self):
        return {'request': self.request}

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

class FollowersListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followers').all()
    serializer_class = FollowersSerializer

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

class FollowingsListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followings').all()
    serializer_class = FollowingsSerializer

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

class AddFollowViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = UserFollow.objects.select_related('follower_id').select_related('following_id').all()
    serializer_class = AddFollowSerializer
    permission_classes = [AddFollowPermission]

    @action(detail=False, methods=['DELETE'])
    def unfollow(self, request):
        follower_id = request.GET.get('follower_id')
        following_id = request.GET.get('following_id')
        follow = get_object_or_404(UserFollow, follower_id=follower_id, following_id=following_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile']
    permission_classes = [PostPermission]

    queryset = Post.objects.filter(is_premium = False).select_related('profile')
    serializer_class = PostSerializer

    @action(detail=False, methods=['GET'])
    def myPosts(self, request):
        profile_id = request.user.profile.id
        if profile_id > 0:
            queryset = Post.objects.filter(profile=profile_id)
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message' : 'you are not an authenticated user'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

class PremiumPostViewSet(ModelViewSet):
    serializer_class = PremiumPostSerializer
    permission_classes = [PremiumPostPermission] 

    def get_queryset(self):
        return Post.objects.filter(profile_id=self.kwargs['profile_pk']).filter(is_premium=True)
    
    def get_serializer_context(self): 
        return {'profile_id': self.kwargs['profile_pk']}
    
class ForMeViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        followings = self.request.user.profile.followings.values_list('following_id')
        subscribed_to = self.request.user.profile.subscribed_to.values_list('profile_id')
        return Post.objects.filter(Q(profile__in=followings) | Q(profile__in=subscribed_to))


class SubscribersViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('subscribers__subscriber_id__user').all()
    serializer_class = SubscribersSerializer

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

class AddSubscriberViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Subscribe.objects.select_related('profile_id').select_related('subscriber_id').all()
    serializer_class = AddSubscriberSerializer
    permission_classes = [SubscribePermission]

    @action(detail=False, methods=['DELETE'])
    def unsubscribe(self, request):
        profile_id = request.GET.get('profile_id')
        subscriber_id = request.GET.get('subscriber_id')
        subscribe = get_object_or_404(Subscribe, profile_id=profile_id, subscriber_id=subscriber_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
