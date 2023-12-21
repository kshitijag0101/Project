from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class IndianCompany(models.Model):
    CIN = models.CharField(max_length=60, unique=True)
    company_name = models.CharField(max_length=255)
    date_of_registration = models.DateField()
    month_name = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    roc = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    Class = models.CharField(max_length=50, null=True)
    company_type = models.CharField(max_length=50, null=True)
    authorized_capital = models.DecimalField(max_digits=50, decimal_places=2, null=True)
    paid_up_capital = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    activity = models.CharField(max_length=255,null=True)
    activity_description = models.TextField(null=True)
    description = models.TextField(null=True)
    registered_office_address = models.TextField()
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    file_name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.CIN


class LLPCompany(models.Model):
    LLPIN = models.CharField(max_length=80, unique=True)
    llp_name = models.CharField(max_length=255)
    founded = models.DateField()
    roc_location = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    industrial_activity = models.CharField(max_length=50)
    activity_description = models.TextField()
    description = models.TextField()
    obligation_of_contribution = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    number_of_partners = models.IntegerField(null=True)
    number_of_designated_partners = models.IntegerField(null=True)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.TextField(null=True)
    month = models.CharField(max_length=20, null=True)
    year = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    file_name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.llp_name

class FCINCompany(models.Model):
    FCIN = models.CharField(max_length=40, unique=True)
    company_name = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=50)
    activity = models.CharField(max_length=50)
    activity_description = models.TextField(null=True)
    description = models.TextField(null=True)
    office_type = models.TextField(null=True)
    address = models.TextField(null=True)
    state = models.CharField(max_length=50)
    month = models.CharField(max_length=20, null=True)
    year = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    file_name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.FCIN

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True)


class StatusCompany(models.Model):
    file_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    fetched_count = models.IntegerField()
    total_count = models.IntegerField()


class fileModel(models.Model):
    file_name = models.TextField()
    data = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True)

class BulkFileModels(models.Model):
    file_name = models.TextField()
    file_url = models.URLField()
    year = models.IntegerField(null=True)
    month = models.CharField(max_length=256, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True)
