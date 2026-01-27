from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPES = (
        ("customer", "customer"),
        ("business", "business"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )

    type = models.CharField(max_length=20, choices=USER_TYPES)

    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")

    file = models.FileField(upload_to="profiles/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.type})"