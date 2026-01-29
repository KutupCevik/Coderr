from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Allows access only to authenticated users with a business profile."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )


class IsOfferOwner(BasePermission):
    """Allows write access only for the creator of the offer."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
