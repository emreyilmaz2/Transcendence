from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class 
User(AbstractUser):
    nickname = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)  # Örnek bir avatar alanı
    friends = models.ManyToManyField('User', related_name='user_friends', blank=True)
    updated = models.DateTimeField (auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    
    def get_friends(self):
        return self.friends.all()
    def get_friends_no(self):
        return self.friends.all().count()
    def __str__(self):
        return self.username
    
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted','accepted'),
)

class Relationship(models.Model):
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"