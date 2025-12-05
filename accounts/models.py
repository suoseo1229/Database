from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
<<<<<<< HEAD
    number = models.CharField(max_length=30)
=======
    number = models.CharField(max_length=30, unique=True)
>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a
    name = models.CharField(max_length=30)
    birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
<<<<<<< HEAD
    nickname = models.CharField(max_length=30)
=======
    
>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a

    def __str__(self):
        self.user.username
