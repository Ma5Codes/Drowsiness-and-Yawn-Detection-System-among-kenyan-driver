from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DriverProfile, Alert, CustomUser, UserSettings

# Register the custom user model with the admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ["user", "ear_threshold", "ear_frames", "yawn_threshold", "alert_frequency"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DriverProfile)
admin.site.register(Alert)
admin.site.register(UserSettings, UserSettingsAdmin)