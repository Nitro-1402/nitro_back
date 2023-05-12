from rest_framework import permissions
from .models import Profile, Subscribe

class IsSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_staff:
                return True
            print(str(request.user.profile.id))
            subscribed_to_list = Profile.objects.filter(user_id=request.user.profile.id).values_list('subscribed_to')
            subscribed_to_list = Subscribe.objects.filter(id__in=subscribed_to_list).values_list('user_id')
            print("subscribed to" + str(subscribed_to_list))
            is_subscribed = False
            print("pofile_pk" + str(view.kwargs['profile_pk']))
            if view.kwargs['profile_pk'] in subscribed_to_list:
                is_subscribed = True
            return bool(is_subscribed)
        return False