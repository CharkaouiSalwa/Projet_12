from epic_events.management.commands.epiceventcommand import EpicEventCommand

class Command(EpicEventCommand):
    help = 'Déconnectez-vous et supprimez le jeton d\'authentification'

    def handle(self, *args, **options):
        # Supprimez le contenu du fichier 'token.txt' pour déconnecter l'utilisateur
        with open('token.txt', 'w') as file:
            file.write('')

        self.stdout.write(self.style.SUCCESS('Déconnexion réussie. Le jeton a été supprimé.'))
