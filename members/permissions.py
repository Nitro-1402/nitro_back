from rest_framework import permissions
from .models import Profile, Subscribe

class IsSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if request.user.profile.id == view.kwargs['profile_pk']:
                return True
            if request.method in permissions.SAFE_METHODS:
                subscribed_to_list = Profile.objects.filter(user_id=request.user.id).values_list('subscribed_to')
                return bool(Profile.objects.filter(
                    id=view.kwargs['profile_pk']).filter(subscribers__in=subscribed_to_list).exists())
        return False