from django.urls import reverse
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
        read_only_fields = ["id"]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return reverse("offerdetail-detail", kwargs={"pk": obj.id})


class OfferListSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name or "",
            "last_name": obj.user.last_name or "",
            "username": obj.user.username,
        }


class OfferRetrieveSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]


class OfferWriteSerializer(serializers.ModelSerializer):
    details = OfferDetailWriteSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("An offer must contain exactly 3 details.")
        types = [d.get("offer_type") for d in value]
        if len(set(types)) != 3:
            raise serializers.ValidationError("Each detail must have a unique offer_type.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        request = self.context["request"]

        offer = Offer.objects.create(user=request.user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for detail in details_data:
                offer_type = detail.get("offer_type")
                if not offer_type:
                    raise serializers.ValidationError({"offer_type": "offer_type is required."})

                try:
                    offer_detail = OfferDetail.objects.get(offer=instance, offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    raise serializers.ValidationError({"details": f"Detail with offer_type '{offer_type}' not found."})

                for field in ["title", "revisions", "delivery_time_in_days", "price", "features"]:
                    if field in detail:
                        setattr(offer_detail, field, detail[field])
                offer_detail.save()

        return instance
