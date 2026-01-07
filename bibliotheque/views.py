from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Media, Membre, Emprunt


# ========== VUE PUBLIQUE (MEMBRES) ==========
def accueil(request):
    """Page d'accueil avec statistiques"""
    # Statistiques REALES
    total_membres = Membre.objects.count()
    total_medias = Media.objects.count()
    medias_disponibles = Media.objects.filter(disponible=True).count()
    emprunts_actifs = Emprunt.objects.filter(date_retour__isnull=True).count()

    context = {
        'total_membres': total_membres,
        'total_medias': total_medias,
        'medias_disponibles': medias_disponibles,
        'emprunts_actifs': emprunts_actifs,
    }

    return render(request, 'bibliotheque/accueil.html', context)


def liste_medias(request):
    """
    APPLICATION MEMBRE
    Permet uniquement d'afficher la liste de tous les médias
    """
    medias = Media.objects.all()

    # Statistiques pour le template
    medias_disponibles = Media.objects.filter(disponible=True).count()

    return render(request, 'bibliotheque/liste_medias.html', {
        'medias': medias,
        'medias_disponibles': medias_disponibles,
    })


# ========== VUES ADMIN (BIBLIOTHÉCAIRES) ==========
@login_required
def liste_membres(request):
    """
    APPLICATION BIBLIOTHÉCAIRE
    Affiche la liste des membres
    """
    if not request.user.is_staff:
        return redirect('liste_medias')

    membres = Membre.objects.all()

    # Statistiques
    total_membres = membres.count()
    membres_actifs = membres.filter(bloque=False).count()
    membres_bloques = membres.filter(bloque=True).count()
    emprunts_actifs = Emprunt.objects.filter(date_retour__isnull=True).count()

    return render(request, 'bibliotheque/liste_membres.html', {
        'membres': membres,
        'total_membres': total_membres,
        'membres_actifs': membres_actifs,
        'membres_bloques': membres_bloques,
        'emprunts_actifs': emprunts_actifs,
    })