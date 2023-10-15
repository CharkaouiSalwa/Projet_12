from django.core.management.base import BaseCommand, CommandError
from epic_events.models import Evenement

class Command(BaseCommand):
    help = 'Mettre à jour les informations d\'un événement'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=str, help='ID de l\'événement à mettre à jour')
        parser.add_argument('--nom_client', type=str, help='Nouveau nom du client', required=False)
        parser.add_argument('--contact_client', type=str, help='Nouveau contact du client', required=False)
        parser.add_argument('--date_debut', type=str, help='Nouvelle date de début', required=False)
        parser.add_argument('--date_fin', type=str, help='Nouvelle date de fin', required=False)
        parser.add_argument('--contact_support', type=str, help='Nouveau contact du support', required=False)
        parser.add_argument('--lieu', type=str, help='Nouveau lieu', required=False)
        parser.add_argument('--participants', type=int, help='Nouveau nombre de participants', required=False)
        parser.add_argument('--notes', type=str, help='Nouvelles notes', required=False)

    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        try:
            event = Evenement.objects.get(event_id=event_id)
        except Evenement.DoesNotExist:
            self.stdout.write(self.style.ERROR('Événement non trouvé.'))
            return

        # Mettez à jour les champs de l'événement s
        for field_name in ['nom_client', 'contact_client', 'date_debut', 'date_fin', 'contact_support', 'lieu', 'participants', 'notes']:
            new_value = kwargs.get(field_name)
            if new_value:
                setattr(event, field_name, new_value)

        event.save()
        self.stdout.write(self.style.SUCCESS(f'Événement {event_id} mis à jour avec succès.'))
