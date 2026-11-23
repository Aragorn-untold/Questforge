from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} id: {self.id}"

    def get_absolute_url(self):
        return reverse("accounts:user-detail", kwargs={"pk": self.pk})


class Profile(models.Model):
    class GenderChoice(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    gender = models.TextField(choices=GenderChoice, default=GenderChoice.OTHER)
    birthday = models.DateField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    # avatar = models.ImageField()
