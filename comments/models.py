from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from members.models import Profile
class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE,null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_okay = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class LikeComment(models.Model):
    LIKETYPE_LIKE = 'L'
    LIKETYPE_DISLIKE = 'D'

    LIKETYPE_CHOICES = [
        (LIKETYPE_LIKE, 'Like'),
        (LIKETYPE_DISLIKE, 'Dislike'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes') 
    like_type = models.CharField(
        max_length=1, choices=LIKETYPE_CHOICES, default=LIKETYPE_LIKE)
    
    class Meta:
        unique_together = [['user', 'comment']]


