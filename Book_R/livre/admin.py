from django.contrib import admin
from .models import Livre

class Livreadmin(admin.ModelAdmin):
    search_fields=('Titre',)
    list_display=('Titre','Auteur','Domaine','Date')

# Register your models here.
admin.site.register(Livre,Livreadmin)