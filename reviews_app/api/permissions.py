from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """Allows access only to authenticated users with a customer profile."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsReviewOwner(BasePermission):
    """Allows write access only for the creator of the review."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
