from django.core.management.base import BaseCommand
from jwt import DecodeError, ExpiredSignatureError
from django.conf import settings
import jwt
from authentication.management.commands.sign_up import User

class EpicEventCommand(BaseCommand):

    def get_authenticated_user(self, token):
        user_id = self.verify_token(token)
        if user_id:
            user = User.objects.filter(id=user_id).first()
            return user
        return None

    help = 'Commande de gestion personnalisée pour Epic Events'

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            return user_id
        except (DecodeError, ExpiredSignatureError):
            return None

    def handle(self, *args, **options):
        # Lisez le token depuis le fichier 'token.txt'
        with open('token.txt', 'r') as file:
            token = file.read().strip()

        user_id = self.verify_token(token)

        if user_id:
            user = self.get_authenticated_user(token)
            if user:
                self.stdout.write(self.style.SUCCESS(f"Utilisateur authentifié avec ID {user_id}, nom {user.username} de l'équipe {user.role}"))
            else:
                self.stdout.write(self.style.ERROR('Utilisateur non trouvé.'))
            self.execute_authenticated_command(*args, **options)
        else:
            self.stdout.write(self.style.ERROR('Authentification échouée. Token invalide ou expiré.'))
