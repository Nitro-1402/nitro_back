from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import *
from movies.models import Movie,News
from movies.serializers import MovieSerializer,NewsSerializer

class CommentRelatedField(serializers.RelatedField):
    
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Movie):
            return MovieSerializer(value).data
        elif isinstance(value, News):
            return NewsSerializer(value).data
        raise Exception('Unexpected type of tagged object')

class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type__model')
    # content_type = ContentTypeRelatedField()
    content_object = CommentRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'message', 'created_at', 'parent_comment', 'user', 'content_type', 'object_id', 'content_object')

    # def get_content_object(self, obj):
    #     content_type = ContentType.objects.get_for_model(obj.content_object.__class__)
    #     serializer = self.context['view'].get_serializer(content_type.model_class())
    #     return serializer.to_representation(obj.content_object)