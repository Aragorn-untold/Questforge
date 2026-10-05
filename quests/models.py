from django.db import models

from campaigns.models import Campaign


class Quest(models.Model):
    class DifficultyChoice(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"
        DEADLY = "DEADLY", "Deadly"

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reward_description = models.TextField()
    difficulty_rating = models.CharField(max_length=10, choices=DifficultyChoice.choices)
    level_recommendation = models.CharField(max_length=60)

    def __str__(self) -> str:
        return f"{self.title} {self.level_recommendation}"

    def to_campaign_quest(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "reward_description": self.reward_description,
            "difficulty_rating": self.difficulty_rating,
            "level_recommendation": self.level_recommendation
        }

    class Meta:
        ordering = ["title"]


class CampaignQuest(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="quests"
    )
    base_quest = models.ForeignKey(
        Quest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campaign_quests"
    )
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reward_description = models.TextField()
    difficulty_rating = models.CharField(max_length=10, choices=Quest.DifficultyChoice.choices)
    level_recommendation = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]
