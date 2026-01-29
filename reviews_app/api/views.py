from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import Review
from .permissions import IsCustomerUser
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """Lists reviews and allows customers to create a new review."""
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Review.objects.all()
        qs = self._apply_filters(qs)
        return self._apply_ordering(qs)

    def _apply_filters(self, qs):
        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            qs = qs.filter(business_user_id=business_user_id)

        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            qs = qs.filter(reviewer_id=reviewer_id)

        return qs

    def _apply_ordering(self, qs):
        ordering = self.request.query_params.get("ordering")
        allowed = ["updated_at", "-updated_at", "rating", "-rating"]
        if ordering in allowed:
            return qs.order_by(ordering)
        return qs.order_by("-updated_at")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

