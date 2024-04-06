from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, user_type=None, **extra_fields):
        """Creates and saves a new user"""
        user_type = user_type or User.UserType.CUSTOMER
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        """Creates and saves a new superuser"""
        user = self.create_user(phone_number, password, user_type=User.UserType.ADMIN)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super().get_queryset()

    def customers(self):
        """Returns queryset of customer users"""
        return self.get_queryset().filter(user_type=User.UserType.CUSTOMER)

    def admins(self):
        """Returns queryset of admin users"""
        return self.get_queryset().filter(user_type=User.UserType.ADMIN)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using phone number as the username"""

    class UserType(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"

    phone_number = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "phone_number"

    # if user changed from customer to admin or vice versa handle its is_staff and is_superuser
    def save(self, *args, **kwargs):
        if self.user_type == self.UserType.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
