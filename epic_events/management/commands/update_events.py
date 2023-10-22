from epic_events.management.commands.epiceventcommand import EpicEventCommand
from epic_events.models import Evenement

class Command(EpicEventCommand):
    help = 'Modifier les événements des supports.'

    def add_arguments(self, parser):
        parser.add_argument('--evenement_id', type=str, help='ID de l\'événement à mettre à jour', required=True)
        parser.add_argument('--nom_client', type=str, help='Nouveau nom du client', required=False)
        parser.add_argument('--date_debut', type=str, help='Nouvelle date de début', required=False)
        parser.add_argument('--date_fin', type=str, help='Nouvelle date de fin', required=False)
        parser.add_argument('--lieu', type=str, help='Nouveau lieu', required=False)
        parser.add_argument('--participants', type=int, help='Nouveau nombre de participants', required=False)
        parser.add_argument('--notes', type=str, help='Nouvelles notes', required=False)

    def handle(self, *args, **options):
        evenement_id = options['evenement_id']
        user = self.get_authenticated_user_from_token_file('token.txt')

        if user and user.role == 'support':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

            try:
                evenement = Evenement.objects.get(event_id=evenement_id, contact_support=user.username)

                # Modifier les champs si les arguments sont fournis
                if 'nom_client' in options:
                    evenement.nom_client = options['nom_client']
                if 'date_debut' in options:
                    evenement.date_debut = options['date_debut']
                if 'date_fin' in options:
                    evenement.date_fin = options['date_fin']
                if 'lieu' in options:
                    evenement.lieu = options['lieu']
                if 'participants' in options:
                    evenement.participants = options['participants']
                if 'notes' in options:
                    evenement.notes = options['notes']

                # Vérifiez si les champs obligatoires sont fournis
                if not evenement.nom_client:
                    self.stdout.write(self.style.ERROR('Le champ "nom_client" est obligatoire.'))
                else:
                    evenement.save()
                    self.stdout.write(self.style.SUCCESS(f'Événement {evenement_id} mis à jour avec succès.'))
            except Evenement.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'L\'événement avec l\'ID {evenement_id} n\'existe pas ou vous n\'avez pas la permission de le modifier.'))
        else:
            self.stdout.write(self.style.ERROR(
                "Utilisateur non trouvé, non authentifié ou n'a pas le rôle 'support'. Veuillez vous connecter et réessayer."))
