from django.core.management.base import BaseCommand
from epic_events.models import Client
from django.utils import timezone
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Mettez à jour les informations d\'un client associé à l\'utilisateur authentifié ayant le rôle "commercial"'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client à mettre à jour')
        parser.add_argument('--nom_complet', type=str, help='Nouveau client', required=False)
        parser.add_argument('--email', type=str, help='Nouvelle adresse mail', required=False)
        parser.add_argument('--telephone', type=str, help='Nouveau numero de telephone', required=False)
        parser.add_argument('--nom_entreprise', type=str, help='Nouvelle entreprise', required=False)
        parser.add_argument('--date_creation', type=str, help='Nouvelle date de création', required=False)
        parser.add_argument('--derniere_mise_a_jour', type=str, help='Dernière mise à jour', required=False)

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'commercial':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            client_id = options['client_id']

            try:
                # Vérifiez si le client existe
                client = Client.objects.get(id=client_id)

                # Mettez à jour les informations du client
                if options['nom_complet']:
                    client.nom_complet = options['nom_complet']
                if options['email']:
                    client.email = options['email']
                if options['telephone']:
                    client.telephone = options['telephone']
                if options['nom_entreprise']:
                    client.nom_entreprise = options['nom_entreprise']
                if options['date_creation']:
                    client.date_creation = options['date_creation']
                if options['derniere_mise_a_jour']:
                    client.derniere_mise_a_jour = options['derniere_mise_a_jour']

                # Mettez à jour les informations du client
                client.derniere_mise_a_jour = timezone.now()
                client.save()

                self.stdout.write(self.style.SUCCESS(f'Les informations du client ont été mises à jour avec succès.'))
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR("Le client spécifié n'a pas été trouvé."))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'commercial'. Veuillez vous connecter et réessayer."))
