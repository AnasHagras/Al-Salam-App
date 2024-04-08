from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    bank_acc_name = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_iban = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_num = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_name_sec = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_iban_sec = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_num_sec = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_name_third = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_iban_third = models.CharField(max_length=30, blank=True, null=True)
    bank_acc_num_third = models.CharField(max_length=30, blank=True, null=True)
    license_number = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    mobile = models.CharField(max_length=256, blank=True, null=True)
    whatsapp = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    representative_name = models.CharField(max_length=256, blank=True, null=True)
    representative_national_id = models.CharField(max_length=256, blank=True, null=True)
    representative_nationality = models.CharField(max_length=256, blank=True, null=True)
    signature_image = models.ImageField(upload_to="company/", blank=True, null=True)
    stamp_image = models.ImageField(upload_to="company/", blank=True, null=True)
    logo_image = models.ImageField(upload_to="company/", blank=True, null=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    class CategoryChoices(models.TextChoices):
        HOME = "home", "Home"
        ABOUT = "about", "About"

    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=256, blank=True, null=True, choices=CategoryChoices.choices, default=CategoryChoices.HOME
    )
    link = models.CharField(max_length=256, blank=True, null=True)

    def get_image_upload_path(instance, filename):
        # Constructing the upload path based on category
        return f"slider/{instance.category}/{filename}"

    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.title
