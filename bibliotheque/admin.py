from django.contrib import admin
from .models import Media, Livre, DVD, CD, JeuPlateau, Membre, Emprunt


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_inscription', 'bloque', 'peut_emprunter_display')
    list_filter = ('bloque', 'date_inscription')
    search_fields = ('nom', 'email')

    def peut_emprunter_display(self, obj):
        return obj.peut_emprunter()

    peut_emprunter_display.boolean = True
    peut_emprunter_display.short_description = "Peut emprunter"


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'type_media', 'annee', 'disponible')
    list_filter = ('type_media', 'disponible', 'annee')
    search_fields = ('titre', 'auteur')


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'isbn', 'pages', 'disponible')


@admin.register(DVD)
class DVDAdmin(admin.ModelAdmin):
    list_display = ('titre', 'realisateur', 'duree', 'disponible')


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ('titre', 'artiste', 'pistes', 'disponible')


@admin.register(JeuPlateau)
class JeuPlateauAdmin(admin.ModelAdmin):
    list_display = ('titre', 'createur', 'joueurs_min', 'joueurs_max')


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('media', 'membre', 'date_emprunt', 'date_retour_prevue', 'date_retour', 'en_retard_display')
    list_filter = ('date_emprunt', 'date_retour')
    search_fields = ('media__titre', 'membre__nom')

    def en_retard_display(self, obj):
        return obj.en_retard()

    en_retard_display.boolean = True
    en_retard_display.short_description = "En retard"
