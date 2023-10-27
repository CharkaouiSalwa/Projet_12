from datetime import  date
from django.utils import timezone
from django.test import TestCase
from unittest.mock import patch
from io import StringIO
from epic_events.models import Client
from django.core.management import call_command


class ListClientCommandTestCase(TestCase):
    def setUp(self):
        # Créez quelques clients de test pour la base de données
        Client.objects.create(nom_complet="Client 1",
                              email="client1@example.com",
                              telephone="1234567890",
                              date_creation=date.today(),
                              nom_entreprise="Entreprise 1",
                              derniere_mise_a_jour=timezone.now())
        Client.objects.create(nom_complet="Client 2",
                              email="client2@example.com",
                              telephone="9876543210",
                              date_creation=date.today(),
                              nom_entreprise="Entreprise 2",
                              derniere_mise_a_jour = timezone.now())

    def test_list_client(self):
        out = StringIO()

        # Utilisez patch pour intercepter la sortie standard (stdout)
        with patch('sys.stdout', out):
            call_command('liste_client')

        # Récupérez la sortie produite par la commande
        output = out.getvalue()

        # Vérifiez que la sortie contient les informations des clients
        self.assertIn("Liste des clients :", output)
        self.assertIn("ID :", output)
        self.assertIn("Nom : Client 1", output)
        self.assertIn("Email : client1@example.com", output)
        self.assertIn("Téléphone : 1234567890", output)
        self.assertIn("Nom de l'entreprise : Entreprise 1", output)
        self.assertIn("ID :", output)
        self.assertIn("Nom : Client 2", output)
        self.assertIn("Email : client2@example.com", output)
        self.assertIn("Téléphone : 9876543210", output)
        self.assertIn("Nom de l'entreprise : Entreprise 2", output)
        self.assertIn("Liste des clients affichée avec succès.", output)

