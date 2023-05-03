from django.db import IntegrityError, transaction
from djoser.serializers import UserCreateSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *

class RWMethodField(serializers.SerializerMethodField):

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        return self.parent.fields[self.field_name].to_representation(data)

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'first_name', 'last_name','email']
    
    email = serializers.SerializerMethodField(write_only=True)

    def update(self, profile:Profile, validated_data):
        profile.user.email = validated_data.pop('email')
        return super().update(profile, validated_data)
    
    def get_email(self, profile:Profile):
        return profile.user.email

class UserCreateSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
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