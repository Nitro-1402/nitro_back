from rest_framework import permissions
from members.models import Profile, Subscribe

class AddToPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                if int(request.user.profile.id) == int(request.data.get('profile')):
                    return True
        else:
            return False