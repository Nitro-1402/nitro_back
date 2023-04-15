from rest_framework import serializers
from .models import *

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo'  , 'first_name' , 'last_name' , 'bio' , 'birth_date']
