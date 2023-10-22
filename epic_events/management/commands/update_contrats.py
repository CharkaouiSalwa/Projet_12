from epic_events.models import Contrat
from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Mettre à jour un contrat en utilisant l\'ID du contrat'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat à mettre à jour')
        parser.add_argument('--montant_total', type=float, help='Nouveau montant total du contrat')
        parser.add_argument('--montant_restant', type=float, help='Nouveau montant restant du contrat')
        parser.add_argument('--date_creation_contrat', type=str, help='Nouvelle date de création du contrat')
        parser.add_argument('--contrat_signe', type=bool, help='Nouvel état du contrat signé (True/False)')

    def execute_authenticated_command(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user = self.get_authenticated_user(token)

        if user:
            if user.role == 'gestion':
                self.stdout.write(self.style.SUCCESS(f'- Bienvenue, {user.username}'))

                contrat_id = options['contrat_id']
                montant_total = options['montant_total']
                montant_restant = options['montant_restant']
                date_creation_contrat = options['date_creation_contrat']
                contrat_signe = options['contrat_signe']

                try:
                    # Recherchez le contrat en fonction de l'ID du contrat
                    contrat = Contrat.objects.get(id=contrat_id)

                    # Mettez à jour les champs du contrat si de nouvelles valeurs sont spécifiées
                    if montant_total is not None:
                        contrat.montant_total = montant_total
                    if montant_restant is not None:
                        contrat.montant_restant = montant_restant
                    if date_creation_contrat is not None:
                        contrat.date_creation_contrat = date_creation_contrat
                    if contrat_signe is not None:
                        contrat.contrat_signe = contrat_signe

                    contrat.save()

                    self.stdout.write(self.style.SUCCESS(f'Contrat mis à jour (ID du contrat : {contrat_id}).'))

                except Contrat.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Contrat avec ID {contrat_id} non trouvé.'))
            else:
                self.stdout.write(self.style.ERROR("Rôle utilisateur non valide."))
        else:
            self.stdout.write(self.style.ERROR('Utilisateur non trouvé ou non authentifié. Veuillez vous connecter et réessayer.'))

