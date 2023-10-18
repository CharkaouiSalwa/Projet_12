
import jwt
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Génère un token JWT pour un utilisateur spécifique'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nom d\'utilisateur')
        parser.add_argument('password', type=str, help='Mot de passe')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            self.stdout.write(self.style.SUCCESS(f'Token JWT généré : {token}'))
        else:
            self.stdout.write(self.style.ERROR('Nom d\'utilisateur ou mot de passe incorrect'))
