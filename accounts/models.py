from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username

