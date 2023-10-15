from django.core.management.base import BaseCommand
from epic_events.models import Evenement

class Command(BaseCommand):
    help = 'Supprimer un événement par son ID'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=str, help='ID de l\'événement à supprimer')

    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']

        try:
            evenement = Evenement.objects.get(event_id=event_id)
            evenement.delete()
            self.stdout.write(self.style.SUCCESS(f'Événement avec l\'ID {event_id} a été supprimé avec succès.'))
        except Evenement.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'L\'événement avec l\'ID {event_id} n\'existe pas.'))
