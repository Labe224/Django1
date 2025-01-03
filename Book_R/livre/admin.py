from django.contrib import admin
from .models import Livre,Historique

class Livreadmin(admin.ModelAdmin):
    search_fields=('Titre',)
    list_display=('Titre','Auteur','Domaine','Date')

# Register your models here.
admin.site.register(Livre,Livreadmin)
admin.site.register(Historique)
