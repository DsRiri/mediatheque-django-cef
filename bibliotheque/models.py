from django.db import models
from datetime import date, timedelta


# ==================== CLASSE MÈRE ====================
class Media(models.Model):
    TYPE_MEDIA = [
        ('LIVRE', 'Livre'),
        ('DVD', 'DVD'),
        ('CD', 'CD'),
        ('JEU', 'Jeu de plateau'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    auteur = models.CharField(max_length=100, verbose_name="Auteur/Réalisateur/Artiste")
    annee = models.IntegerField(verbose_name="Année de publication")
    type_media = models.CharField(max_length=10, choices=TYPE_MEDIA, verbose_name="Type")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ['titre']

    def __str__(self):
        return f"{self.titre} ({self.auteur}, {self.annee})"

    def emprunter(self, membre):
        if self.disponible and membre.peut_emprunter() and self.type_media != 'JEU':
            emprunt = Emprunt.objects.create(
                media=self,
                membre=membre,
                date_retour_prevue=date.today() + timedelta(days=7)
            )
            self.disponible = False
            self.save()
            return emprunt
        return None


# ==================== CLASSES ENFANTS ====================
class Livre(Media):
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN", blank=True, null=True)
    pages = models.IntegerField(verbose_name="Nombre de pages", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type_media = 'LIVRE'
        super().save(*args, **kwargs)


class DVD(Media):
    realisateur = models.CharField(max_length=100, verbose_name="Réalisateur")
    duree = models.IntegerField(verbose_name="Durée (minutes)", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type_media = 'DVD'
        super().save(*args, **kwargs)


class CD(Media):
    artiste = models.CharField(max_length=100, verbose_name="Artiste")
    pistes = models.IntegerField(verbose_name="Nombre de pistes", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type_media = 'CD'
        super().save(*args, **kwargs)


# ==================== JEU DE PLATEAU ====================
class JeuPlateau(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre du jeu")
    createur = models.CharField(max_length=100, verbose_name="Créateur")
    joueurs_min = models.IntegerField(default=1, verbose_name="Joueurs minimum")
    joueurs_max = models.IntegerField(default=4, verbose_name="Joueurs maximum")

    class Meta:
        verbose_name = "Jeu de plateau"
        verbose_name_plural = "Jeux de plateau"

    def __str__(self):
        return f"{self.titre} (créé par {self.createur})"


# ==================== MEMBRE ====================
class Membre(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    date_inscription = models.DateField(auto_now_add=True, verbose_name="Date d'inscription")
    bloque = models.BooleanField(default=False, verbose_name="Membre bloqué")

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    def peut_emprunter(self):
        emprunts_actifs = self.emprunt_set.filter(date_retour__isnull=True)
        return not self.bloque and emprunts_actifs.count() < 3

    def __str__(self):
        return f"{self.nom} ({self.email})"


# ==================== EMPRUNT ====================
class Emprunt(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Média")
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, verbose_name="Membre")
    date_emprunt = models.DateField(auto_now_add=True, verbose_name="Date d'emprunt")
    date_retour_prevue = models.DateField(verbose_name="Date de retour prévue")
    date_retour = models.DateField(null=True, blank=True, verbose_name="Date de retour effective")

    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"

    def en_retard(self):
        if self.date_retour:
            return False
        return date.today() > self.date_retour_prevue

    def __str__(self):
        statut = "✅ Retourné" if self.date_retour else ("⚠️ En retard" if self.en_retard() else "📅 En cours")
        return f"{self.membre.nom} - {self.media.titre} ({statut})"