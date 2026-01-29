from django.urls import reverse
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
        read_only_fields = ["id"]

