from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    phone = models.CharField(verbose_name="شماره تلفن", max_length=11)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"
        
# Create your models here.
