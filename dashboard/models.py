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
