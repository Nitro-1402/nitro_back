from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count,Sum
from rest_framework import serializers
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
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    def get_like_count(self, comment:Comment):
        return comment.likes.filter(like_type = 'L').count()
    
    def get_dislike_count(self, comment:Comment):
        return comment.likes.filter(like_type = 'D').count()
        
    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'parent_comment', 'user',
                   'is_okay', 'content_type', 'object_id', 'content_object',
                   'like_count', 'dislike_count']
        
class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id', 'comment', 'user', 'like_type']

class LikedCommentsSerializer(serializers.ModelSerializer):
    liked_comments = serializers.SerializerMethodField()

    def get_liked_comments(self, liked_comment:LikeComment):
        return liked_comment.comment.id 

    class Meta:
        model = LikeComment
        fields = ['liked_comments']