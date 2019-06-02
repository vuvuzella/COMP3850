from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users of an object to edit
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # always allow GET, HEAD and OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # other actions, check if user is the owner of the object 
        return obj.user == request.user
