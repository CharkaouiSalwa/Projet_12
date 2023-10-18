from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Permet à un utilisateur de s\'inscrire'

    def handle(self, *args, **kwargs):
        # Demander à l'utilisateur de fournir les informations nécessaires
        username = input('Nom d\'utilisateur: ')
        password = input('Mot de passe: ')
        first_name = input('Prénom: ')
        last_name = input('Nom de famille: ')
        email = input('Adresse e-mail: ')
        telephone = input('Numéro de téléphone: ')
        role = input('Rôle/Poste: ')

        # Vérifiez si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'L\'utilisateur avec le nom d\'utilisateur {username} existe déjà.'))
            return

        # Créez un nouvel utilisateur
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, telephone=telephone, role=role)

        self.stdout.write(self.style.SUCCESS(f'L\'utilisateur {user.username} a été créé avec succès.'))


