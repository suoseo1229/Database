from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        self.user.username
