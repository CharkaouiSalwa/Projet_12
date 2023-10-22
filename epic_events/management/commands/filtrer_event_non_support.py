from django.db.models import Q
from epic_events.management.commands.epiceventcommand import EpicEventCommand
from epic_events.models import Evenement

class Command(EpicEventCommand):
    help = 'Affiche les événements sans contact_support.'

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'gestion':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            evenements = Evenement.objects.filter(Q(contact_support__isnull=True) | Q(contact_support=''))

            if evenements.exists():
                self.stdout.write('Événements sans contact_support:')
                for evenement in evenements:
                    self.stdout.write(f'ID de l\'événement: {evenement.event_id}')
                    self.stdout.write(f'Nom du client: {evenement.nom_client}')
                    self.stdout.write(f'Date de début: {evenement.date_debut}')
                    self.stdout.write(f'Date de fin: {evenement.date_fin}')
                    self.stdout.write(f'Lieu: {evenement.lieu}')
                    self.stdout.write(f'Nombre de participants: {evenement.participants}')
                    self.stdout.write(f'Contact Support: {evenement.contact_support}')
                    self.stdout.write(f'Notes: {evenement.notes}')
                    self.stdout.write("\n")
            else:
                self.stdout.write(self.style.SUCCESS('Aucun événement sans contact_support trouvé.'))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'gestion'. Veuillez vous connecter et réessayer."))
