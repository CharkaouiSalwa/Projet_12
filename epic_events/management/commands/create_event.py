from django.core.management.base import BaseCommand
from epic_events.models import Evenement, Contrat

class Command(BaseCommand):
    help = 'Crée un événement pour un contrat signé d\'un client.'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat auquel ajouter l\'événement')

    def handle(self, *args, **kwargs):
        contrat_id = kwargs['contrat_id']

        try:
            contrat = Contrat.objects.get(id=contrat_id)
        except Contrat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Le contrat avec l\'ID {contrat_id} n\'existe pas.'))
            return

        # Demandez les informations de l'événement à créer.
        event_id = input('ID de l\'événement : ')
        nom_client = input('Nom du client : ')
        contact_client = input('Contact du client : ')
        date_debut = input('Date de début (AAAA-MM-JJ HH:MM:SS) : ')
        date_fin = input('Date de fin (AAAA-MM-JJ HH:MM:SS) : ')
        contact_support = input('Contact du support : ')
        lieu = input('Lieu : ')
        participants = input('Nombre de participants : ')
        notes = input('Notes : ')

        # Créez l'objet événement.
        event = Evenement(event_id=event_id, nom_client=nom_client, contact_client=contact_client,
                          date_debut=date_debut, date_fin=date_fin, contact_support=contact_support, lieu=lieu,
                          participants=participants, notes=notes)
        event.save()

        # Ajoutez l'événement au contrat.
        contrat.evenements.add(event)

        self.stdout.write(
            self.style.SUCCESS(f'Événement créé avec succès pour le contrat {contrat.identifiant_unique}.'))