from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user or request.user.is_superuser)


class IsPartnerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role in
            ('admin', 'partner') or request.user.is_superuser
        )


class IsPartnerOwner(permissions.BasePermission):
    """
    Check if user with Partner role is owner of establishment or beverage
    """
    def has_object_permission(self, request, view, obj):
        direct_owner = hasattr(obj, 'owner') and obj.owner == request.user

        establishment_owner = hasattr(obj, 'establishment') and \
                              hasattr(obj.establishment, 'owner') and \
                              obj.establishment.owner == request.user

        return bool(direct_owner or establishment_owner or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsPartnerAndAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role in
            ('admin', 'partner') or request.user.is_superuser
        )


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)


class IsAuthenticatedAndNotAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role != 'admin' and not request.user.is_superuser
        )
