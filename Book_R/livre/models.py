from django.db import models

class Livre(models.Model):
    Id= models.AutoField(primary_key=True)
    Titre = models.CharField(max_length=245)
    Auteur = models.CharField(max_length=245)
    Domaine= models.CharField(max_length=245)
    Date = models.CharField(max_length=10)
    Description=models.CharField(max_length=345)
    Image=models.ImageField(upload_to="livre_image/")
    pdf=models.FileField(upload_to="livre_pdf/")


# Create your models here.
