from rest_framework import serializers
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Full serializer for listing and retrieving orders."""
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order based on an OfferDetail id."""
    offer_detail_id = serializers.IntegerField()
