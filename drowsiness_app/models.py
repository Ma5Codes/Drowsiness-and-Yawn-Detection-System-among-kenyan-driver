from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="custom_user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.email


class DriverProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="driver_profile",
    )
    license_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Alert(models.Model):
    driver = models.ForeignKey(
        DriverProfile, on_delete=models.CASCADE, related_name="alerts"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(
        max_length=50,
        choices=(
            ("drowsiness", "Drowsiness"),
            ("yawning", "Excessive Yawning"),
            # Add more alert types as needed
        ),
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.alert_type} - {self.driver.user.username} ({self.timestamp})"


class UserSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_settings",
    )
    ear_threshold = models.FloatField(default=0.3)
    ear_frames = models.IntegerField(default=30)
    yawn_threshold = models.IntegerField(default=20)
    alert_frequency = models.CharField(
        max_length=10,
        choices=(
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ),
        default="medium",
    )

    def __str__(self):
        return f"{self.user.username}'s Settings"