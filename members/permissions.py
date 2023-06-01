from rest_framework import permissions
from .models import Profile, Subscribe

class PremiumPostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif int(request.user.profile.id) == int(view.kwargs['profile_pk']):
                    return True
            elif request.method in permissions.SAFE_METHODS:
                return bool(Profile.objects.filter(
                    id=view.kwargs['profile_pk']).filter(subscribers__subscriber_id=request.user.profile.id).exists())
        return False
    
class ProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                if request.user.profile.id == Profile.objects.get(id=view.kwargs['pk']).id:
                    return True
        else:
            return False
        
class AddFollowPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                if int(request.user.profile.id) == int(request.data.get('follower_id')):
                    return True
        else:
            return False
        
class PostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif request.method == 'POST':
                if int(request.user.profile.id) == int(request.data.get('profile')):
                    return True
            else:
                return bool(Profile.objects.filter(id=request.user.profile.id, post__in=view.kwargs['pk']).exists())
        else:
            return False
        
class SubscribePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                if int(request.user.profile.id) == int(request.data.get('subscriber_id')):
                    return True
        else:
            return False