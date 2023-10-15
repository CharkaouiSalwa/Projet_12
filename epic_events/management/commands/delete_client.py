from django.core.management.base import BaseCommand
from epic_events.models import Client

class Command(BaseCommand):
    help = 'Supprimer un client par son ID'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client à supprimer')

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']

        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            self.stdout.write(self.style.SUCCESS(f'Client avec ID {client_id} a été supprimé avec succès.'))
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Le client avec l\'ID {client_id} n\'existe pas.'))
