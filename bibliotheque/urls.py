"""
URLs pour l'application bibliotheque
"""

from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),

    # Application membre (public)
    path('medias/', views.liste_medias, name='liste_medias'),

    # Application bibliothécaire (admin seulement)
    path('membres/', views.liste_membres, name='liste_membres'),
]