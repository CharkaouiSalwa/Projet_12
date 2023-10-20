from django.core.management.base import BaseCommand
from epic_events.models import Client
from datetime import date
from django.utils import timezone
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Crée un client associé à l\'utilisateur authentifié ayant le rôle "commercial"'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--token', type=str, help='Token JWT', required=True)

    def execute_authenticated_command(self, *args, **options):
        user = self.get_authenticated_user(options['token'])

        if user and user.role == 'commercial':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            # Demandez à l'utilisateur de fournir les informations nécessaires pour créer un client
            nom_complet = input('Nom complet du client: ')
            email = input('Adresse e-mail du client: ')
            telephone = input('Numéro de téléphone du client: ')
            nom_entreprise = input('Nom de l\'entreprise du client: ')

            # Créez un nouveau client
            client = Client.objects.create(
                nom_complet=nom_complet,
                email=email,
                telephone=telephone,
                nom_entreprise=nom_entreprise,
                date_creation=date.today(),
                derniere_mise_a_jour=timezone.now(),
                contact_commercial=user
            )

            self.stdout.write(self.style.SUCCESS(f'Le client {client.nom_complet} a été créé avec succès.'))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'commercial'. Veuillez vous connecter et réessayer."))
