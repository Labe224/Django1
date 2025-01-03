from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from livre.models import Historique
from .models import Profile
from datetime import timedelta,datetime

def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request):
    # Si la méthode est POST, tenter de connecter l'utilisateur
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentifier l'utilisateur avec les identifiants
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si l'authentification réussit, connecter l'utilisateur
            login(request, user)
            return redirect('home')  # Rediriger vers la page d'accueil

        else:
            # Si l'authentification échoue, afficher un message d'erreur
            messages.info(request, "Identifiants ou mot de passe incorrect")

    # Si l'utilisateur est déjà authentifié, récupérer son profil
    if request.user.is_authenticated:
        try:
            # Récupérer le profil de l'utilisateur connecté
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Si aucun profil n'existe pour cet utilisateur, gérer l'exception
        historique=Historique.objects.filter(user=request.user)
        return render(request, 'accounts/login.html', {'profile': profile,'historique':historique})

    return render(request, 'accounts/login.html')



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email_address = request.POST.get('email_address')
        niveau_etude = request.POST.get('niveau_etude')
        Nom= request.POST.get('Nom')
        Prenom=request.POST.get('Prenom')
        password_confirm=request.POST.get('password_confirm')

        # Créer l'utilisateur
        if User.objects.filter(username=username).exists():
            messages.info(request,"le nom d'utilisateur existe déjà")
            return render(request, 'accounts/register.html', {'nom':Nom,'email':email_address,'prenom':Prenom,'etude':niveau_etude,'username':username})
        elif password!=password_confirm:
            messages.info(request,"les deux mots de pass ne sont pas identiques")
            return render(request, 'accounts/register.html', {'nom':Nom,'email':email_address,'prenom':Prenom,'etude':niveau_etude,'username':username})
        else:
           user = User.objects.create_user(username=username, password=password)
           # Créer le profil avec les informations supplémentaires
           profile = Profile.objects.create(
             user=user,
             email_address=email_address,
             niveau_etude=niveau_etude,
             Nom=Nom,
             Prenom=Prenom,
           )
           return redirect('accounts:login')  # Rediriger vers la page d'accueil

    else:
       return render(request, 'accounts/register.html')
def historique(request):
    histo = Historique.objects.filter(user=request.user)  # Récupère les historiques de l'utilisateur
    date = datetime.now().date()  # Obtenir l'heure actuelle
    for historique in histo:
        delta = date - historique.date  
        if delta > timedelta(days=2):
            historique.delete()
    
    return render(request,'accounts/historique.html',{'historique':histo})

def modif_profil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_username = request.POST.get('new')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=request.user.username).exists():
            profile = Profile.objects.get(user=request.user)
            
            # Vérification et mise à jour du mot de passe
            if new_username == '' and password != '' and email == '':
                if password != password_confirm:
                    messages.info(request, "Les deux mots de passe ne sont pas identiques.")
                    return render(request, 'accounts/modif.html', {'username': username, 'new_username': new_username})
                else:
                    user = request.user
                    profile.user.set_password(password)
                    user.save()
                    profile.save()
                    messages.success(request, "Mot de passe modifié avec succès.")
                    return redirect('accounts:login')  # Redirige vers la page de profil après la mise à jour du mot de passe

            # Mise à jour du nom d'utilisateur
            if new_username != '' and password == '' and email == '':
                if User.objects.filter(username=new_username).exists():
                    messages.info(request, "Ce nom d'utilisateur existe déjà.")
                    return render(request, 'accounts/modif.html', {'message': messages})
                else:
                    user = request.user
                    profile.user.username = new_username
                    user.save()
                    profile.save()
                    messages.success(request, "Nom d'utilisateur modifié avec succès.")
                    return redirect('accounts:login')  # Redirige vers la page de profil

            # Mise à jour de l'email
            if email != '' and password == '' and new_username == '':
                user = request.user
                profile.email_address = email
                user.save()
                profile.save()
                messages.success(request, "Email modifié avec succès.")
                return redirect('accounts:login')  # Redirige vers la page de profil

            # Mise à jour de tous les champs (nom d'utilisateur, mot de passe, email)
            if new_username != '' and password != '' and email != '':
                if User.objects.filter(username=new_username).exists():
                    messages.info(request, "Ce nom d'utilisateur existe déjà.")
                    return render(request, 'accounts/modif.html', {'message': messages})
                else:
                    if password != password_confirm:
                        messages.info(request, "Les deux mots de passe ne sont pas identiques.")
                        return render(request, 'accounts/modif.html', {'username': username, 'new_username': new_username})

                    user = request.user
                    profile.user.username = new_username
                    profile.user.set_password(password)
                    profile.email_address = email
                    user.save()
                    profile.save()
                    messages.success(request, "Profil modifié avec succès.")
                    return redirect('accounts:login')  # Redirige vers la page de profil

        else:
            messages.error(request, "Utilisateur non trouvé.")
            return render(request, 'accounts/modif.html', {'username': username, 'new_username': new_username})
    
    return render(request, 'accounts/modif.html', {'username': request.user.username, 'new_username': '', 'email': request.user.email})



# Create your views here.
