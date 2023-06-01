from django.db import IntegrityError, transaction
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import *

# class RWMethodField(serializers.SerializerMethodField):

#     def __init__(self, method_name=None, **kwargs):
#         self.method_name = method_name
#         kwargs['source'] = '*'
#         super().__init__(**kwargs)
    
#     def to_internal_value(self, data):
#         return self.parent.fields[self.field_name].to_representation(data)
    
class EmailUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['email']

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'first_name', 'last_name', 'user', 'is_followed']
    
    user = EmailUserSerializer(read_only=False)

    is_followed = serializers.SerializerMethodField()

    def get_is_followed(self, profile:Profile):
        me = self.context['request'].user
        if me.is_authenticated and not me.is_staff:
            return bool(Profile.objects.filter(id=profile.id).filter(followers__follower_id=me.profile.id).exists())
        else:
            return False


    def update(self, instance:Profile, validated_data):
        if validated_data.get('photo') is not None:
            instance.photo = validated_data.get('photo')
        if validated_data.get('first_name') is not None:
            instance.first_name = validated_data.get('first_name')
        if validated_data.get('last_name') is not None:
            instance.last_name = validated_data.get('last_name')
        if validated_data.get('user') is not None:
            email_field = validated_data.get('user')['email']
            user_instace = User.objects.get(id=instance.user.id)
            user_instace.email = email_field
            instance.user.email = email_field
            user_instace.save()
        
        instance.save()
        return instance


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
            return "http://nitroback.pythonanywhere.com" + str(user_follow.follower_id.photo.url)
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
            return "http://nitroback.pythonanywhere.com" + str(user_follow.following_id.photo.url)
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

class PostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'first_name', 'last_name', 'username']

    photo = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_photo(self, profile:Profile):
        if profile.photo:
            return "http://nitroback.pythonanywhere.com" + str(profile.photo.url)
        return
    
    def get_username(self, profile:Profile):
        return profile.user.username


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'body', 'profile_id', 'profile', 'is_premium']

    is_premium = serializers.BooleanField(read_only=True)

    profile = PostProfileSerializer()


    def create(self, validated_data):
        return Post.objects.create(is_premium=False, **validated_data)

class PremiumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'body']
    
    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Post.objects.create(profile_id=profile_id, is_premium=True, **validated_data)

class AddSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['profile_id', 'subscriber_id']

class SubscriberInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['username', 'photo']
    
    username = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    def get_username(self, subscribe:Subscribe):
        return subscribe.subscriber_id.user.username
    
    def get_photo(self, subscribe:Subscribe):
        if subscribe.subscriber_id.photo:
            return "http://nitroback.pythonanywhere.com" + str(subscribe.subscriber_id.photo.url)
        return

class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['subscribers']
    
    subscribers = SubscriberInstanceSerializer(many=True)
