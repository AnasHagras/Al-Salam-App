from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["phone_number", "name"]
    fieldsets = (
        (None, {"fields": ("phone_number", "user_type")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("phone_number", "password1", "password2")}),)


admin.site.register(User, UserAdmin)
