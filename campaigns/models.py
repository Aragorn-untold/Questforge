from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Campaign(models.Model):
    class ActiveChoice(models.TextChoices):
        NOT_STARTED = "inactive", "Inactive"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        ENDED = "ended", "Ended"

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="campaigns"
    )
    created_at = models.DateField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    last_updated = models.DateField(auto_now=True)
    is_active = models.CharField(
        max_length=30, choices=ActiveChoice, default=ActiveChoice.NOT_STARTED
    )
    ended = models.DateField(null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("campaigns:campaign-detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-created_at"]


class CampaignNote(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="campaign_notes")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# class CampaignMessage(models.Model):
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="messages")
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="campaign_messages")
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
