
from django.core.management.base import BaseCommand
import sentry_sdk

class Command(BaseCommand):
    help = 'un test de sentry'

    def handle(self, *args, **options):
        raise Exception("Ceci est un test de Sentry.")
