from django.db import models
from users.models import User
from django.utils import timezone


class LoginOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return f"user_id={self.user.id}, otp={self.otp}"

    def save(self, *args, **kwargs):
        # If expiry_at is not set, set it to current time + 5 minutes
        if not self.expiry_at:
            self.expiry_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expiry_at and self.expiry_at <= timezone.now()
