from rest_framework import permissions

class AddToPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                if int(request.user.profile.id) == int(request.GET.get('profile')):
                    return True
        else:
            return False