from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="offers/", null=True, blank=True)
    description = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
