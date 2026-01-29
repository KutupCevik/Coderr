from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from offers_app.models import OfferDetail
from orders_app.models import Order
from .permissions import IsCustomerUser, IsBusinessUser, IsStaffUser, IsOrderBusinessOwner
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD for orders with role-based permissions."""
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        if self.action == "partial_update":
            return OrderStatusSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated(), IsCustomerUser()]
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBusinessUser(), IsOrderBusinessOwner()]
        if self.action == "destroy":
            return [IsAuthenticated(), IsStaffUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_detail = self._get_offer_detail(serializer.validated_data["offer_detail_id"])
        order = self._create_order_from_detail(request.user, offer_detail)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def _get_offer_detail(self, offer_detail_id):
        try:
            return OfferDetail.objects.select_related("offer", "offer__user").get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return None

    def _create_order_from_detail(self, customer_user, offer_detail):
        if offer_detail is None:
            raise ValueError("OfferDetail not found.")

        offer = offer_detail.offer
        business_user = offer.user

        return Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer=offer,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

    def handle_exception(self, exc):
        if isinstance(exc, ValueError):
            return Response({"detail": "Offer detail not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
