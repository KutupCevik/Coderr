from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allows access only to authenticated users with a customer profile."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsBusinessUser(BasePermission):
    """Allows access only to authenticated users with a business profile."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )


class IsStaffUser(BasePermission):
    """Allows access only to staff users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOrderBusinessOwner(BasePermission):
    """Allows access only if the order belongs to the business user."""
    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
