from rest_framework import serializers
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving reviews."""
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Creates a review for a business user by the authenticated customer."""
    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        business_user = attrs["business_user"]

        if not hasattr(business_user, "profile") or business_user.profile.type != "business":
            raise serializers.ValidationError({"business_user": "User is not a business profile."})

        exists = Review.objects.filter(
            business_user=business_user, reviewer=request.user
        ).exists()
        if exists:
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this business user."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        return Review.objects.create(reviewer=request.user, **validated_data)
