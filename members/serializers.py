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

