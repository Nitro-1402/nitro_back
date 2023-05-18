from rest_framework import permissions
from members.models import Profile, Subscribe

class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if request.method == 'POST':
                return True
            if Profile.objects.filter(id=request.user.profile.id,comment__in=view.kwargs['pk']).exists():
                return True
            if request.method in permissions.SAFE_METHODS:
                subscribed_to_list = Profile.objects.filter(user_id=request.user.id).values_list('subscribed_to')
                return bool(Profile.objects.filter(
                    id=view.kwargs['profile_pk']).filter(subscribers__in=subscribed_to_list).exists())
        else:
            return False