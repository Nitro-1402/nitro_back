from rest_framework import permissions
from .models import Profile

class IsSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        subscribed_to_list = Profile.objects.filter(user_id=request.user.id).values_list('subscribed_to')
        is_subscribed = False
        if view.kwargs['profile_pk'] in subscribed_to_list:
            is_subscribed = True
        return bool(request.user and is_subscribed) or bool(request.user.is_staff)