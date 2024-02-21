from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)  # Örnek bir avatar alanı

    def __str__(self):
        return self.username
