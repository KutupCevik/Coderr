from django.db.models import Min, Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from offers_app.models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOfferOwner
from .serializers import (
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferWriteSerializer,
    OfferDetailWriteSerializer,
)


class OfferPagination(PageNumberPagination):
    """PageNumberPagination with adjustable page_size."""
    page_size_query_param = "page_size"


class OfferViewSet(viewsets.ModelViewSet):
    """Offers CRUD with public list and restricted create/update/delete."""
    pagination_class = OfferPagination

    def get_queryset(self):
        qs = self._base_queryset()
        qs = self._apply_filters(qs)
        qs = self._apply_search(qs)
        return self._apply_ordering(qs)

    def _base_queryset(self):
        return (
            Offer.objects.select_related("user")
            .prefetch_related("details")
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def _apply_filters(self, qs):
        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            qs = qs.filter(user_id=creator_id)

        min_price = self.request.query_params.get("min_price")
        if min_price:
            qs = qs.filter(min_price__gte=min_price)

        max_delivery_time = self.request.query_params.get("max_delivery_time")
        if max_delivery_time:
            qs = qs.filter(min_delivery_time__lte=max_delivery_time)

        return qs

    def _apply_search(self, qs):
        search = self.request.query_params.get("search")
        if not search:
            return qs
        return qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    def _apply_ordering(self, qs):
        ordering = self.request.query_params.get("ordering")
        allowed = ["updated_at", "-updated_at", "min_price", "-min_price"]
        if ordering in allowed:
            return qs.order_by(ordering)
        return qs

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action in ["partial_update", "destroy"]:
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return OfferListSerializer
        if self.action == "retrieve":
            return OfferRetrieveSerializer
        return OfferWriteSerializer


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only access to offer details for authenticated users."""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailWriteSerializer
    permission_classes = [IsAuthenticated]
