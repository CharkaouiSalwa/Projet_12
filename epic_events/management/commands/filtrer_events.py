from django.core.management.base import BaseCommand
from epic_events.models import Evenement, Contrat

class Command(BaseCommand):
    help = 'Affiche les événements attribués à un contrat et tous les événements si aucun ID de contrat n\'est fourni.'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, nargs='?', help='ID du contrat (facultatif)')

    def handle(self, *args, **kwargs):
        contrat_id = kwargs['contrat_id']

        if contrat_id is not None:
            try:
                contrat = Contrat.objects.get(id=contrat_id)
                evenements = contrat.evenements.all()
                self.stdout.write(f'Événements attribués au contrat {contrat.identifiant_unique}:')
            except Contrat.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Le contrat avec l\'ID {contrat_id} n\'existe pas.'))
                return
        else:
            evenements = Evenement.objects.all()
            self.stdout.write('Tous les événements:')

        for evenement in evenements:
            self.stdout.write(f'ID de l\'événement: {evenement.event_id}')
            self.stdout.write(f'Nom du client: {evenement.nom_client}')
            self.stdout.write(f'Date de début: {evenement.date_debut}')
            self.stdout.write(f'Date de fin: {evenement.date_fin}')
            self.stdout.write(f'Lieu: {evenement.lieu}')
            self.stdout.write(f'Nombre de participants: {evenement.participants}')
            self.stdout.write(f'Notes: {evenement.notes}')





