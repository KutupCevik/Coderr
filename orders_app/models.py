from django.db import models
from django.contrib.auth.models import User
from offers_app.models import Offer, OfferDetail


class Order(models.Model):
    """Stores an order created by a customer based on an OfferDetail snapshot."""

    STATUS_CHOICES = (
        ("in_progress", "in_progress"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    )

    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders_as_customer"
    )
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders_as_business"
    )

    offer = models.ForeignKey(Offer, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    offer_detail = models.ForeignKey(OfferDetail, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")

    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.FloatField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} ({self.status})"
