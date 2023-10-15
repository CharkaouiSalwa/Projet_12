from django.core.management.base import BaseCommand
from epic_events.models import Contrat

class Command(BaseCommand):
    help = 'Supprimer un contrat par son ID'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat à supprimer')

    def handle(self, *args, **kwargs):
        contrat_id = kwargs['contrat_id']

        try:
            contrat = Contrat.objects.get(id=contrat_id)
            contrat.delete()
            self.stdout.write(self.style.SUCCESS(f'Contrat avec l\'ID {contrat_id} a été supprimé avec succès.'))
        except Contrat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Le contrat avec l\'ID {contrat_id} n\'existe pas.'))
