from epic_events.management.commands.epiceventcommand import EpicEventCommand
from epic_events.models import Evenement


class Command(EpicEventCommand):
    help = "Attribuer un support à un événement qui n'a pas de contact_support."

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, help='ID de l\'événement à mettre à jour')
        parser.add_argument('--contact_support', type=str, help='Nom du support à attribuer à l\'événement',
                            required=False)

    def handle(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and (user.role == 'gestion' or user.role == 'support'):
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            evenement_id = options['evenement_id']
            contact_support = options['contact_support']

            try:
                evenement = Evenement.objects.get(event_id=evenement_id)

                # Vérifiez si l'événement n'a pas de contact_support

                if evenement.contact_support is None or evenement.contact_support.strip() == '':
                    if contact_support:
                        # Ajoutez le support à l'événement
                        evenement.contact_support = contact_support
                        evenement.save()
                        self.stdout.write(self.style.SUCCESS(
                            f'Le support "{contact_support}" a été attribué à l\'événement (ID de l\'événement : {evenement_id}).'))
                    else:
                        self.stdout.write(
                            self.style.ERROR('L\'argument --contact_support est requis pour attribuer un support.'))
                else:
                    self.stdout.write(self.style.ERROR('Cet événement a déjà un contact_support.'))
            except Evenement.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'L\'événement avec l\'ID {evenement_id} n\'existe pas.'))
        else:
            self.stdout.write(self.style.ERROR(
                "Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'gestion' ou 'support'. Veuillez vous connecter et réessayer."))
