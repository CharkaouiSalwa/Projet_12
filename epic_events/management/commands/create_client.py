from django.core.management.base import BaseCommand, CommandError
from epic_events.models import Client
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Créer un client en l\'associant automatiquement à l\'utilisateur authentifié'

    def handle(self, *args, **kwargs):
        # Demandez à l'utilisateur de fournir les informations nécessaires pour créer un client
        nom_complet = input('Nom complet du client: ')
        email = input('Adresse e-mail du client: ')
        telephone = input('Numéro de téléphone du client: ')
        nom_entreprise = input('Nom de l\'entreprise du client: ')

        # Obtenez l'utilisateur actuellement authentifié
        username = self.get_input_data('Nom d\'utilisateur: ')
        user = User.objects.filter(username=username).first()

        if not user:
            self.stdout.write(self.style.ERROR('Utilisateur non trouvé. Veuillez vous connecter et réessayer.'))
            return

        # Créez un nouveau client et associez-le automatiquement à l'utilisateur actuellement authentifié
        client = Client.objects.create(
            nom_complet=nom_complet,
            email=email,
            telephone=telephone,
            nom_entreprise=nom_entreprise,
            date_creation=date.today(),
            derniere_mise_a_jour=timezone.now(),
            contact_commercial=user
        )

        self.stdout.write(self.style.SUCCESS(f'Le client {client.nom_complet} a été créé avec succès et est associé à l\'utilisateur {user.username}.'))

    def get_input_data(self, prompt):
        try:
            return input(prompt)
        except EOFError:
            raise CommandError("Abandon.")

