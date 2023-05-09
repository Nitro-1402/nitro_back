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
            return value.title
        elif isinstance(value, News):
            return value.title
        raise Exception('Unexpected type of tagged object')

class CommentSerializer(serializers.ModelSerializer):
    content_object = CommentRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'parent_comment', 'user',
                   'is_okay', 'content_type', 'object_id', 'content_object']
        
class CreateLike(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id', 'comment', 'user', 'like_type']