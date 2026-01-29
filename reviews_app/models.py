from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    """A customer review for a business user. Only one review per reviewer+business."""
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_received"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_written"
    )
    rating = models.IntegerField()
    description = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"],
                name="unique_review_per_business_and_reviewer",
            )
        ]

    def __str__(self):
        return f"Review {self.id} ({self.rating})"
