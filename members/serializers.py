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

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo', 'username']
    
    photo = serializers.SerializerMethodField()
    def get_photo(self, user:User):
        return user.profile.photo

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['following_id']

    following_id = SimpleUserSerializer(many=True)