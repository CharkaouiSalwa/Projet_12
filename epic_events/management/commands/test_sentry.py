
from django.core.management.base import BaseCommand
import sentry_sdk

class Command(BaseCommand):
    help = 'un test de sentry'

    def handle(self, *args, **options):
        try:
            raise Exception("Ceci est un test de Sentry.")
        except Exception as e:
            # Capturez l'exception et signalez-la à Sentry
            with sentry_sdk.configure_scope() as scope:
                scope.set_extra("command_name", "test_sentry")
            sentry_sdk.capture_exception(e)
            self.stdout.write(self.style.ERROR(f'Erreur : {str(e)}'))
