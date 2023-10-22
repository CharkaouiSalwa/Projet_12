from epic_events.models import Client, Contrat
from django.utils import timezone
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Créer un contrat'

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'gestion':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))
            return user  # Retournez l'utilisateur authentifié
        else:
            self.stdout.write(self.style.ERROR("L'utilisateur n'est pas autorisé à créer un contrat."))
            return None

    def handle(self, *args, **options):
        # Vérifiez l'authentification de l'utilisateur
        user = self.execute_authenticated_command(*args, **options)
        if not user:
            return

        # Demandez à l'utilisateur de fournir les informations nécessaires pour créer un contrat
        client_id = input('ID du client associé au contrat: ')
        identifiant_unique = input('Identifiant unique du contrat: ')
        montant_total = input('Montant total du contrat: ')
        montant_restant = input('Montant restant à payer: ')

        date_creation_contrat = input('Date de création du contrat (AAAA-MM-JJ): ')
        contrat_signe = input('Contrat signé (True/False): ').lower() == 'true'

        try:
            date_creation_contrat = timezone.make_aware(timezone.datetime.strptime(date_creation_contrat, '%Y-%m-%d'))
        except ValueError:
            self.stdout.write(self.style.ERROR('Format de date invalide. Utilisez le format AAAA-MM-JJ.'))
            return

        client = Client.objects.filter(id=client_id).first()

        if not client:
            self.stdout.write(self.style.ERROR('Client introuvable. Veuillez spécifier un client existant.'))
            return

        # Créez le contrat en associant le champ contact_commercial à l'utilisateur connecté
        contrat = Contrat.objects.create(
            client=client,
            identifiant_unique=identifiant_unique,
            contact_commercial=user,
            montant_total=montant_total,
            montant_restant=montant_restant,
            date_creation_contrat=date_creation_contrat,
            contrat_signe=contrat_signe
        )

        self.stdout.write(self.style.SUCCESS(f'Le contrat {contrat.identifiant_unique} a été créé avec succès.'))
