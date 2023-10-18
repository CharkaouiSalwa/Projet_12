from django.core.management.base import BaseCommand
from epic_events.models import Contrat
from .epiceventcommand import EpicEventCommand


class Command(EpicEventCommand):
    help = 'Supprimer un contrat par son ID'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat à supprimer')
        parser.add_argument('token', type=str, help='Token JWT à utiliser pour l\'authentification')


    def handle(self, *args, **kwargs):
        contrat_id = kwargs['contrat_id']
        token = kwargs['token']

        try:
            contrat = Contrat.objects.get(id=contrat_id)
            contrat.delete()
            self.stdout.write(self.style.SUCCESS(f'Contrat avec l\'ID {contrat_id} a été supprimé avec succès.'))
        except Contrat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Le contrat avec l\'ID {contrat_id} n\'existe pas.'))
