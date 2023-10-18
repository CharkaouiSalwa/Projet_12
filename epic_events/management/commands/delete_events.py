from django.core.management.base import BaseCommand
from epic_events.models import Evenement
from .epiceventcommand import EpicEventCommand


class Command(EpicEventCommand):
    help = 'Supprimer un événement par son ID'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=str, help='ID de l\'événement à supprimer')
        parser.add_argument('token', type=str, help='Token JWT à utiliser pour l\'authentification')


    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        token = kwargs['token']

        try:
            evenement = Evenement.objects.get(event_id=event_id)
            evenement.delete()
            self.stdout.write(self.style.SUCCESS(f'Événement avec l\'ID {event_id} a été supprimé avec succès.'))
        except Evenement.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'L\'événement avec l\'ID {event_id} n\'existe pas.'))
