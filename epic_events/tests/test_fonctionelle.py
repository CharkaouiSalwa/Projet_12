from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class FunctionalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test1',
            password='test111'
        )
        self.token_file = 'token.txt'

    def tearDown(self):
        self.user.delete()
        if os.path.exists(self.token_file):
            os.remove(self.token_file)

    def test_login_list_logout(self):
        # Connexion de l'utilisateur
        call_command('login', 'test1', 'test111', '--file', self.token_file)

        # Assurez-vous que le fichier de jeton JWT a été créé
        self.assertTrue(os.path.exists(self.token_file))

        # Liste des clients
        call_command('liste_client')

        # Déconnexion de l'utilisateur
        call_command('logout')

        # Assurez-vous que le contenu du fichier de jeton JWT a été supprimé
        with open(self.token_file, 'r') as file:
            token_contents = file.read()
        self.assertEqual(token_contents, "")