from django.shortcuts import render,redirect
from accounts.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Livre,Historique

def home(request):
    livre=Livre.objects.all()
    if request.method == 'GET':
        name=request.GET.get('recherche')
        if not name==None:
          livres=Livre.objects.filter(Titre__icontains=name)
          return render(request,'livre/resulatat.html',{'livres':livres})
    return render(request,'livre/accueil.html', {'livre':livre})
# Create your views here.

def type(request,Domaine):
    livre=Livre.objects.filter(Domaine=Domaine)
    if request.method == 'GET':
        name=request.GET.get('recherche')
        if not name==None:
          livres=Livre.objects.filter(Titre__icontains=name)
          return render(request,'livre/resulatat.html',{'livres':livres})
    return render(request, 'livre/domaine.html',{'livre':livre,'domaine':Domaine})

@csrf_exempt

def livre(request, Titre):
    livre=Livre.objects.get(Titre=Titre)
    if request.user.is_authenticated:
      utilisateur=request.user
   
      historique = Historique.objects.filter(user=utilisateur, livre=livre).first()

      if historique:
        # Si l'historique existe, on met à jour la date de lecture
        historique.date = timezone.now()
        historique.save()
      else:
        # Si l'historique n'existe pas, on crée un nouvel enregistrement
        historique = Historique.objects.create(
            user=utilisateur,
            livre=livre,
            date=timezone.now(),  # Enregistrer la date de lecture
        )
        historique.save()

    if request.method=='POST':
        note=int(request.POST.get('note',0))
        if note in [1,2,3,4,5]:
            livre.Note=(livre.Note*livre.Nb_lecture+note)/(livre.Nb_lecture+1)
            livre.Note=round(livre.Note,1)
            livre.Nb_lecture+=1
            livre.save()
            redirect('livre',Titre=livre.Titre)

    return render(request,'livre/livre.html',{"livre":livre})

def lecteur_pdf(request, Titre):
   livre=Livre.objects.get(Titre=Titre)
   if request.user.is_authenticated:
      utilisateur=request.user
   
      historique = Historique.objects.filter(user=utilisateur, livre=livre).first()

      if historique:
        # Si l'historique existe, on met à jour la date de lecture
        historique.date = timezone.now()
        historique.save()
      else:
        try:
            # Récupérer le profil de l'utilisateur connecté
            profile = Profile.objects.get(user=request.user)
            profile.lecture+=1
            profile.save()
        except Profile.DoesNotExist:
            profile = None  # Si aucun profil n'existe pour cet utilisateur, gérer l'exception
        # Si l'historique n'existe pas, on crée un nouvel enregistrement
        historique = Historique.objects.create(
            user=utilisateur,
            livre=livre,
            date=timezone.now(),  # Enregistrer la date de lecture
        )
        historique.save()
       
   
   return render(request,'livre/lecteur.html',{'livre':livre})