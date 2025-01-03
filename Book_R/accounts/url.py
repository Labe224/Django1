from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('login',views.login_user,name='login'),
    path('register',views.register_user,name='register'),
    path('logout',views.logout_user,name='logout'),
    path('historique',views.historique,name='historique'),
    path('modification',views.modif_profil,name='modif')
]