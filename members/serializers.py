from django.db import IntegrityError, transaction
from djoser.serializers import UserCreateSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo'  , 'first_name' , 'last_name' , 'bio' , 'birth_date']

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

class AddFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ['follower_id', 'following_id']
 