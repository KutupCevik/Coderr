from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=["customer", "business"])

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )

        username = attrs["username"]
        email = attrs["email"]

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "This username is already taken."}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)