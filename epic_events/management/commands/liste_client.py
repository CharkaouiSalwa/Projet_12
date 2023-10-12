from django.core.management.base import BaseCommand
from epic_events.models import Client

class Command(BaseCommand):
    help = 'Afficher la liste des clients'

    def handle(self, *args, **options):
        clients = Client.objects.all()

        self.stdout.write("Liste des clients :")
        for client in clients:
            self.stdout.write(f"ID : {client.id}")
            self.stdout.write(f"Nom : {client.nom_complet}")
            self.stdout.write(f"Email : {client.email}")
            self.stdout.write(f"Téléphone : {client.telephone}")
            self.stdout.write(f"Nom de l'entreprise : {client.nom_entreprise}")
            self.stdout.write(f"Date de création : {client.date_creation}")
            self.stdout.write(f"Dernière mise à jour : {client.derniere_mise_a_jour}")
            self.stdout.write(f"Contact commercial : {client.contact_commercial}")
            self.stdout.write("\n")

        self.stdout.write(self.style.SUCCESS('Liste des clients affichée avec succès.'))
