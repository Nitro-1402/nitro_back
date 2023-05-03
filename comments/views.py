from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import *
from .serializers import *

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user').select_related('parent_comment').select_related('content_type').all()
    serializer_class = CommentSerializer
