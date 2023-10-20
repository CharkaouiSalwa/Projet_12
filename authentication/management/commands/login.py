import jwt
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Génère un token JWT pour un utilisateur spécifique et l\'enregistre dans un fichier'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nom d\'utilisateur')
        parser.add_argument('password', type=str, help='Mot de passe')
        parser.add_argument('--file', type=str, help='Nom du fichier de sortie', default='token.txt')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        output_file = kwargs['file']

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            payload = {
                'user_id': user.id
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            # Enregistrez le token dans le fichier spécifié
            with open(output_file, 'w') as file:
                file.write(token)

            self.stdout.write(self.style.SUCCESS(f'Token JWT généré et enregistré dans {output_file}'))
        else:
            self.stdout.write(self.style.ERROR('Nom d\'utilisateur ou mot de passe incorrect'))
