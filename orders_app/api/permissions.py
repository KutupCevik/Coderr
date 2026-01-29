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
