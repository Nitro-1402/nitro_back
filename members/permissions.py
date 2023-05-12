from rest_framework import permissions
from .models import Profile, Subscribe

class IsSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_staff:
                return True
            print(str(request.user.id))
            subscribed_to_list = Profile.objects.filter(user_id=request.user.id).values_list('subscribed_to')
            return bool(Profile.objects.filter(
                id=view.kwargs['profile_pk']).filter(subscribers__in=subscribed_to_list).exists())
            print("subscribed to" + str(subscribed_to_list))
            is_subscribed = False
            print("pofile_pk" + str(view.kwargs['profile_pk']))
            if view.kwargs['profile_pk'] in subscribed_to_list:
                is_subscribed = True
            return bool(is_subscribed)
        return False