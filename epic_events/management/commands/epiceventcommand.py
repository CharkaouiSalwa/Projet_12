from django.core.management.base import BaseCommand
from jwt import DecodeError, ExpiredSignatureError
from django.conf import settings
import jwt

from authentication.management.commands.sign_up import User

class EpicEventCommand(BaseCommand):

    def get_authenticated_user(self, token):
        user_id = self.verify_token(token)
        if user_id:
            return User.objects.filter(id=user_id).first()
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
        token = options.get('token')
        user_id = self.verify_token(token)

        if user_id:
            self.stdout.write(self.style.SUCCESS(f'Utilisateur authentifié avec ID {user_id}'))
            self.execute_authenticated_command(*args, **options)
        else:
            self.stdout.write(self.style.ERROR('Authentification échouée. Token invalide ou expiré.'))
