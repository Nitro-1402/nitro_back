from django.db import IntegrityError, transaction
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *

class RWMethodField(serializers.SerializerMethodField):

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        return self.parent.fields[self.field_name].to_representation(data)
    
class EmailUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['email']

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'first_name', 'last_name','user']
    
    user = EmailUserSerializer(read_only=False)


class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            profile = Profile.objects.create(user_id=user.id)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

class FollowerInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ['username', 'photo']
    
    username = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    def get_username(self, user_follow:UserFollow):
        return user_follow.follower_id.user.username
    
    def get_photo(self, user_follow:UserFollow):
        if user_follow.follower_id.photo:
            return user_follow.follower_id.photo
        return
    

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['followers']
    
    followers = FollowerInstanceSerializer(many=True)

class FollowingInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ['username', 'photo']
    
    username = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    def get_username(self, user_follow:UserFollow):
        return user_follow.following_id.user.username
    
    def get_photo(self, user_follow:UserFollow):
        if user_follow.following_id.photo:
            return user_follow.following_id.photo
        return
    

class FollowingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['followings']
    
    followings = FollowingInstanceSerializer(many=True)

class AddFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ['follower_id', 'following_id']

class WatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['watched_list']