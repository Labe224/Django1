# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField(unique=True, blank=True, null=True)
    Nom = models.CharField(blank=True, null=True,max_length=100)
    Prenom =models.CharField(blank=True,null=True,max_length=100)
    lecture =models.IntegerField(default=0)
    niveau_etude = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
