from django.utils import timezone
from epic_events.models import Evenement, Contrat
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Crée un événement pour un contrat signé d\'un client.'

    # Utilisez la méthode execute_authenticated_command pour vérifier le token et le rôle
    def execute_authenticated_command(self, *args, **options):
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user and user.role == 'commercial':
            self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))
            return True
        else:
            self.stdout.write(self.style.ERROR('Authentification échouée. Token invalide ou utilisateur non autorisé.'))
            return False

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat auquel ajouter l\'événement')

    def handle(self, *args, **kwargs):
        if self.execute_authenticated_command(**kwargs):
            contrat_id = kwargs['contrat_id']

            try:
                contrat = Contrat.objects.get(id=contrat_id)
            except Contrat.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Le contrat avec l\'ID {contrat_id} n\'existe pas.'))
                return

            if contrat.contrat_signe:
                # Le reste du code pour créer l'événement
                event_id = input('ID de l\'événement : ')
                nom_client = input('Nom du client : ')
                contact_client = input('Contact du client : ')
                date_debut = input('Date de début (AAAA-MM-JJ HH:MM:SS) : ')
                date_fin = input('Date de fin (AAAA-MM-JJ HH:MM:SS) : ')
                contact_support = input('Contact du support : ')
                lieu = input('Lieu : ')
                participants = input('Nombre de participants : ')
                notes = input('Notes : ')

                event = Evenement(
                    event_id=event_id,
                    nom_client=nom_client,
                    contact_client=contact_client,
                    date_debut=timezone.now(),
                    date_fin=timezone.now(),
                    contact_support=contact_support,
                    lieu=lieu,
                    participants=participants,
                    notes=notes
                )
                event.save()

                contrat.evenements.add(event)

                self.stdout.write(
                    self.style.SUCCESS(f'Événement créé avec succès pour le contrat {contrat.identifiant_unique}.'))
            else:
                self.stdout.write(
                    self.style.ERROR('Le contrat n\'est pas signé, vous ne pouvez pas créer d\'événement.'))
