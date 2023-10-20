from django.core.management.base import BaseCommand
from epic_events.models import Client
from django.utils import timezone
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Mettez à jour les informations d\'un client associé à l\'utilisateur authentifié ayant le rôle "commercial"'

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'commercial':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            # Demandez à l'utilisateur de saisir l'ID du client à mettre à jour
            client_id = input('ID du client à mettre à jour : ')

            # Vérifiez si le client existe
            client = Client.objects.filter(id=client_id).first()
            if not client:
                self.stdout.write(self.style.ERROR("Le client spécifié n'a pas été trouvé."))
                return

            # Demandez à l'utilisateur de fournir les informations mises à jour pour le client
            client.nom_complet = input('Nouveau nom complet du client (laissez vide pour ne pas mettre à jour) : ') or client.nom_complet
            client.email = input('Nouvelle adresse e-mail du client (laissez vide pour ne pas mettre à jour) : ') or client.email
            client.telephone = input('Nouveau numéro de téléphone du client (laissez vide pour ne pas mettre à jour) : ') or client.telephone
            client.nom_entreprise = input('Nouveau nom de l\'entreprise du client (laissez vide pour ne pas mettre à jour) : ') or client.nom_entreprise

            # Mettez à jour les informations du client
            client.derniere_mise_a_jour = timezone.now()
            client.save()

            self.stdout.write(self.style.SUCCESS(f'Les informations du client ont été mises à jour avec succès.'))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'commercial'. Veuillez vous connecter et réessayer."))
