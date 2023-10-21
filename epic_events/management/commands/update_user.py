from django.core.management.base import BaseCommand
from epic_events.models import Collaborateur
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Modifier un utilisateur si l\'utilisateur authentifié a le rôle "gestion".'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID de l\'utilisateur à modifier')
        parser.add_argument('--nom_utilisateur', type=str, help='Nouveau nom d\'utilisateur')
        parser.add_argument('--email', type=str, help='Nouvelle adresse e-mail')
        parser.add_argument('--role', type=str, help='Nouveau rôle de l\'utilisateur')

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'gestion':
            self.stdout.write(self.style.SUCCESS(f'Utilisateur authentifié avec ID {user.id}, nom {user.username}, et rôle {user.role}.'))
            return True
        else:
            self.stdout.write(self.style.ERROR("L'utilisateur n'est pas autorisé à modifier un utilisateur."))
            return False

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        new_username = kwargs['nom_utilisateur']
        new_email = kwargs['email']
        new_role = kwargs['role']

        # Vérifiez l'authentification de l'utilisateur
        authenticated = self.execute_authenticated_command(*args, **kwargs)

        if authenticated:
            try:
                user_to_update = Collaborateur.objects.get(id=user_id)
            except Collaborateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'L\'utilisateur avec l\'ID {user_id} n\'existe pas.'))
                return

            # Mettez à jour les informations de l'utilisateur
            if new_username:
                user_to_update.username = new_username
            if new_email:
                user_to_update.email = new_email
            if new_role:
                user_to_update.role = new_role

            user_to_update.save()

            self.stdout.write(self.style.SUCCESS(f'Utilisateur mis à jour avec succès.'))
        else:
            self.stdout.write(self.style.ERROR("L'utilisateur n'est pas autorisé à modifier un utilisateur."))
