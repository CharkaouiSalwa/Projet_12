from epic_events.management.commands.epiceventcommand import EpicEventCommand
from epic_events.models import Evenement
from django.db.models import Q


class Command(EpicEventCommand):
    help = 'Affiche les événements des Supports.'

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'support':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            # Recherchez les événements où le contact_support est le nom d'utilisateur du support actuel ou le contact_support est nul.
            evenements = Evenement.objects.filter(Q(contact_support=user.username) | Q(contact_support__isnull=True))

            if evenements.exists():
                self.stdout.write('Événements des supports:')
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
                self.stdout.write(self.style.SUCCESS('Aucun événement avec contact_support trouvé.'))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'support'. Veuillez vous connecter et réessayer."))
