from django.core.management.base import BaseCommand
from epic_events.models import Collaborateur
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Supprimer un utilisateur si l\'utilisateur authentifié a le rôle "gestion".'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID de l\'utilisateur à supprimer')

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'gestion':
            self.stdout.write(self.style.SUCCESS(f'Utilisateur authentifié avec ID {user.id}, nom {user.username}, et rôle {user.role}.'))
            return True
        else:
            self.stdout.write(self.style.ERROR("L'utilisateur n'est pas autorisé à supprimer un utilisateur."))
            return False

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']

        # Vérifiez l'authentification de l'utilisateur
        authenticated = self.execute_authenticated_command(*args, **kwargs)

        if authenticated:
            try:
                user_to_delete = Collaborateur.objects.get(id=user_id)
            except Collaborateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'L\'utilisateur avec l\'ID {user_id} n\'existe pas.'))
                return

            # Supprimez l'utilisateur
            user_to_delete.delete()

            self.stdout.write(self.style.SUCCESS(f'Utilisateur supprimé avec succès.'))
        else:
            self.stdout.write(self.style.ERROR("L'utilisateur n'est pas autorisé à supprimer un utilisateur."))
