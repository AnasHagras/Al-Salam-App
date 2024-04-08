from django.db import models


# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=255, default="Default Settings")
    app_version = models.CharField(max_length=255, default="1.0.0")
    app_description = models.TextField(default="Default Description")
    android_link = models.CharField(
        max_length=255, default="https://play.google.com/store/apps/details?id=com.example.app"
    )
    ios_link = models.CharField(max_length=255, default="https://apps.apple.com/us/app/app-name/id1234567890")
    is_banner_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to="application/", blank=True, null=True)

    def __str__(self):
        return self.name
