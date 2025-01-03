from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
import os
class Livre(models.Model):
    Id= models.AutoField(primary_key=True)
    Titre = models.CharField(max_length=245)
    Auteur = models.CharField(max_length=245)
    Domaine= models.CharField(max_length=245)
    Date = models.CharField(max_length=10)
    Description=models.CharField(max_length=345)
    Image=models.ImageField(upload_to="livre_image/", blank=True, null=True)
    pdf=models.FileField(upload_to="livre_pdf/")
    Note=models.FloatField(default=0)
    Nb_lecture=models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        # Ajouter une image par défaut si le domaine est "Informatique" et aucune image n'est fournie
        if self.Domaine == 'Informatique' and not self.Image:
            self.Image = 'livre_image/defaut_informatique.png'
        
        # Appeler la méthode save() de la classe parente pour enregistrer l'instance
        super(Livre, self).save(*args, **kwargs)

        # Si une image a été téléchargée, redimensionner l'image
        if self.Image:
            self.redimensionner_image()

    def redimensionner_image(self):
        # Ouvrir l'image avec Pillow
        img = Image.open(self.Image)

        # Définir la taille maximale (par exemple, 175x1571 pixels)
        max_size = (180, 160)

        # Redimensionner l'image tout en gardant les proportions
        img.thumbnail(max_size)

        # Sauvegarder l'image redimensionnée dans le même fichier
        img.save(self.Image.path)  # Sauvegarde de l'image redimensionnée à l'emplacement d'origine

class Historique(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   livre=models.ForeignKey(Livre, on_delete=models.CASCADE)
   date=models.DateField(default=datetime.now)

    
            
