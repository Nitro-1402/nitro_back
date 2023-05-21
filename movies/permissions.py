from rest_framework import permissions
from members.models import Profile, Subscribe

class RatingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif request.method == 'POST':
                if int(request.user.profile.id) == int(request.data.get('profile')):
                    return True
            elif request.method == 'DELETE'  or request.method == 'PUT' or request.method == 'PATCH':
                return bool(Profile.objects.filter(id=request.user.profile.id,rating__in=view.kwargs['pk']).exists())
        else:
            return False