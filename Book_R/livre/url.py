from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('livre/<str:Domaine>/',views.type,name='domaine'),
    path('<str:Titre>/',views.livre,name='livre'),
    path('lecteur/<str:Titre>',views.lecteur_pdf, name='lecteur')
    
    
]