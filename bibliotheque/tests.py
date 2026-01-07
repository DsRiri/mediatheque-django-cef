from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Membre, Livre, DVD, CD, JeuPlateau, Emprunt
from datetime import date, timedelta


class ModelTests(TestCase):
    def test_creation_membre(self):
        """Test création d'un membre"""
        membre = Membre.objects.create(
            nom="Test User",
            email="test@example.com"
        )
        self.assertEqual(membre.nom, "Test User")
        self.assertEqual(membre.email, "test@example.com")
        self.assertFalse(membre.bloque)

    def test_membre_peut_emprunter(self):
        """Test contrainte métier: max 3 emprunts"""
        membre = Membre.objects.create(nom="Test", email="test@test.com")
        self.assertTrue(membre.peut_emprunter())

    def test_creation_livre(self):
        """Test création d'un livre"""
        livre = Livre.objects.create(
            titre="Python pour débutants",
            auteur="Jean Dupont",
            annee=2023,
            isbn="9781234567890",
            pages=300
        )
        self.assertEqual(livre.type_media, 'LIVRE')
        self.assertTrue(livre.disponible)

    def test_creation_dvd(self):
        """Test création d'un DVD"""
        dvd = DVD.objects.create(
            titre="Inception",
            auteur="Christopher Nolan",
            annee=2010,
            realisateur="Christopher Nolan",
            duree=148
        )
        self.assertEqual(dvd.type_media, 'DVD')

    def test_emprunt_retard(self):
        """Test détection de retard d'emprunt"""
        membre = Membre.objects.create(nom="Test", email="test@test.com")
        livre = Livre.objects.create(
            titre="Test", auteur="Auteur", annee=2023,
            isbn="123", pages=100
        )

        emprunt = Emprunt.objects.create(
            media=livre,
            membre=membre,
            date_retour_prevue=date.today() - timedelta(days=1)
        )
        self.assertTrue(emprunt.en_retard())


class ViewTests(TestCase):
    def setUp(self):
        # Créer un utilisateur admin pour les tests
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )

        # Créer un membre et un média pour les tests
        self.membre = Membre.objects.create(nom="Alice", email="alice@test.com")
        self.livre = Livre.objects.create(
            titre="Test Livre", auteur="Auteur", annee=2023,
            isbn="123", pages=100
        )

    def test_accueil_page(self):
        """Test page d'accueil"""
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bibliotheque/accueil.html')

    def test_liste_medias_page(self):
        """Test page liste médias"""
        response = self.client.get(reverse('liste_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bibliotheque/liste_medias.html')

    def test_liste_membres_page_non_authentifie(self):
        """Test page membres sans authentification"""
        response = self.client.get(reverse('liste_membres'))
        # Doit rediriger vers liste_medias si non admin
        self.assertEqual(response.status_code, 302)

    def test_liste_membres_page_authentifie(self):
        """Test page membres avec authentification admin"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('liste_membres'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bibliotheque/liste_membres.html')

    def test_admin_interface(self):
        """Test interface admin Django"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class URLTests(TestCase):
    def test_urls(self):
        """Test que toutes les URLs existent"""
        urls = [
            reverse('accueil'),
            reverse('liste_medias'),
            reverse('liste_membres'),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])  # 302 pour redirections


# Tests des contraintes métier
class BusinessRulesTests(TestCase):
    def test_max_3_emprunts(self):
        """Test qu'un membre ne peut pas avoir plus de 3 emprunts"""
        membre = Membre.objects.create(nom="Test", email="test@test.com")

        # Créer 3 livres
        livres = []
        for i in range(3):
            livre = Livre.objects.create(
                titre=f"Livre {i}", auteur="Auteur", annee=2023,
                isbn=f"123{i}", pages=100
            )
            livres.append(livre)

        # Créer 3 emprunts
        for livre in livres:
            Emprunt.objects.create(
                media=livre,
                membre=membre,
                date_retour_prevue=date.today() + timedelta(days=7)
            )
            livre.disponible = False
            livre.save()

        # Vérifier que le membre ne peut plus emprunter
        self.assertFalse(membre.peut_emprunter())

    def test_jeu_non_empruntable(self):
        """Test qu'un jeu de plateau n'est pas empruntable"""
        jeu = JeuPlateau.objects.create(
            titre="Monopoly",
            createur="Charles Darrow"
        )

        # Un jeu n'a pas de champ 'disponible' comme les autres médias
        # et ne devrait pas apparaître dans les listes d'emprunt
        self.assertFalse(hasattr(jeu, 'disponible'))
