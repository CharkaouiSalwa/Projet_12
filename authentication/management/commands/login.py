from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Connectez-vous en tant qu\'utilisateur'

    def handle(self, *args, **kwargs):
        username = input('Nom d\'utilisateur: ')
        password = input('Mot de passe: ')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            self.stdout.write(self.style.SUCCESS(f'Connexion réussie en tant que {user.username}'))
        else:
            self.stdout.write(self.style.ERROR('Nom d\'utilisateur ou mot de passe incorrect'))
