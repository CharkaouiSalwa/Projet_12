from django.core.management.base import BaseCommand
from epic_events.models import Client, Contrat
from django.utils import timezone

class Command(BaseCommand):
    help = 'Créer un contrat '

    def handle(self, *args, **options):
        # Demandez à l'utilisateur de fournir les informations nécessaires pour créer un contrat
        client_id = input('ID du client associé au contrat: ')
        identifiant_unique = input('Identifiant unique du contrat: ')
        contact_commercial = input('Nom du contact commercial: ')
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

        contrat = Contrat.objects.create(
            client=client,
            identifiant_unique=identifiant_unique,
            contact_commercial=contact_commercial,
            montant_total=montant_total,
            montant_restant=montant_restant,
            date_creation_contrat=date_creation_contrat,
            contrat_signe=contrat_signe
        )

        self.stdout.write(self.style.SUCCESS(f'Le contrat {contrat.identifiant_unique} a été créé avec succès.'))
