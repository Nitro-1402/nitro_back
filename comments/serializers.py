from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.model')

    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'message', 'created_at', 'parent_comment', 'user', 'content_type', 'object_id', 'content_object')

    def get_content_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj.content_object.__class__)
        serializer = self.context['view'].get_serializer(content_type.model_class())
        return serializer.to_representation(obj.content_object)