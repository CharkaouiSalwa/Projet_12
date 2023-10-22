from epic_events.models import Evenement
from django.utils import timezone
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Mettez à jour les informations des événements des supports'

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, help='ID de l\'événement à mettre à jour')
        parser.add_argument('--nom_client', type=str, help='Nouveau client', required=False)
        parser.add_argument('--contrat', type=str, help='Nouveau contrat', required=False)
        parser.add_argument('--contact_client', type=str, help='Nouveau contact client', required=False)
        parser.add_argument('--date_debut', type=str, help='Nouvelle date de début', required=False)
        parser.add_argument('--date_fin', type=str, help='Nouvelle date de fin', required=False)
        parser.add_argument('--lieu', type=str, help='Nouveau lieu', required=False)
        parser.add_argument('--participants', type=int, help='Nouveau nombre de participants', required=False)
        parser.add_argument('--notes', type=str, help='Nouvelle note', required=False)

    def handle(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'support':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            evenement_id = options['evenement_id']

            try:
                # Vérifiez si l'événement existe
                evenement = Evenement.objects.get(event_id=evenement_id, contact_support=user.username)

                # Mettez à jour les informations de l'événement en fonction des arguments fournis
                if options['nom_client']:
                    evenement.nom_client = options['nom_client']
                if options['contrat']:
                    evenement.contrat = options['contrat']
                if options['contact_client']:
                    evenement.contact_client = options['contact_client']
                if options['date_debut']:
                    evenement.date_debut = options['date_debut']
                if options['date_fin']:
                    evenement.date_fin = options['date_fin']
                if options['lieu']:
                    evenement.lieu = options['lieu']
                if options['participants']:
                    evenement.participants = options['participants']
                if options['notes']:
                    evenement.notes = options['notes']

                # Mettez à jour la date de dernière modification de l'événement
                evenement.derniere_mise_a_jour = timezone.now()
                evenement.save()

                self.stdout.write(self.style.SUCCESS("Les informations de l'événement ont été mises à jour avec succès."))
            except Evenement.DoesNotExist:
                self.stdout.write(self.style.ERROR("L'événement spécifié n'a pas été trouvé."))
        else:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'support'. Veuillez vous connecter et réessayer."))
