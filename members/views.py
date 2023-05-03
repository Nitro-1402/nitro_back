from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins
from .models import *
from .serializers import *
from .forms import Profilephoto


class TokenObtainPairViewWithUserId(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['access']
        user_id = self.token_user_id(token)
        return Response({
            'access': token,
            'refresh': response.data['refresh'],
            'user_id': user_id,
        })

    def token_user_id(self, token):
        decoded_token = self.get_token_object(token).payload
        return decoded_token.get('user_id')

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = EditProfileSerializer

class FollowersListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followers').all()
    serializer_class = FollowersSerializer

class FollowingsListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followings').all()
    serializer_class = FollowingsSerializer

class AddFollowViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = UserFollow.objects.select_related('follower_id').select_related('following_id').all()
    serializer_class = AddFollowSerializer

class DeleteFollowViewSet(APIView):
    def delete(self, request):
        follower_id = request.GET.get('follower_id')
        following_id = request.GET.get('following_id')
        follow = get_object_or_404(UserFollow, follower_id=follower_id, following_id=following_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def profilephotoview(request):
    if request.method == 'POST' :
        form = Profilephoto(request.POST , request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Profilephoto()