from django.core.management.base import BaseCommand
from epic_events.models import Client

class Command(BaseCommand):
    help = 'Mettre à jour les informations d\'un client'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client à mettre à jour')
        parser.add_argument('--nom_complet', type=str, help='Nouveau nom complet du client', required=False)
        parser.add_argument('--email', type=str, help='Nouvelle adresse e-mail du client', required=False)
        parser.add_argument('--telephone', type=str, help='Nouveau numéro de téléphone du client', required=False)
        parser.add_argument('--nom_entreprise', type=str, help='Nouveau nom de l\'entreprise du client', required=False)

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR('Client non trouvé.'))
            return

        # Mettez à jour les champs du client si des valeurs ont été spécifiées
        for field_name in ['nom_complet', 'email', 'telephone', 'nom_entreprise']:
            new_value = kwargs.get(field_name)
            if new_value:
                setattr(client, field_name, new_value)

        client.save()
        self.stdout.write(self.style.SUCCESS(f'Client {client_id} mis à jour avec succès.'))
