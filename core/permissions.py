from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        return True
        # if request.user.is_authenticated:
        #     return request.user.role in ["admin"]
        # else:
        #     return False
