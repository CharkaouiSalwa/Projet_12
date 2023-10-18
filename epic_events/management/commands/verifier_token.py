from .epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Commande spécifique pour Epic Events'

    def add_arguments(self, parser):
        parser.add_argument('token', type=str, help='Token JWT à vérifier')

    def execute_authenticated_command(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Commande spécifique exécutée avec succès.'))
