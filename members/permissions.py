from rest_framework import permissions
from .models import Profile

class IsSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_staff:
                return True
            subscribed_to_list = Profile.objects.filter(user_id=request.user.id).values_list('subscribed_to')
            is_subscribed = False
            if view.kwargs['profile_pk'] in subscribed_to_list:
                is_subscribed = True
            return bool(is_subscribed)
        return False