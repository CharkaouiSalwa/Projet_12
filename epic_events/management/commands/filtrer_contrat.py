from django.core.management.base import BaseCommand
from epic_events.models import Contrat

class Command(BaseCommand):
    help = 'Filtrer et afficher des contrats en fonction de certaines conditions.'

    def add_arguments(self, parser):
        parser.add_argument('--non_signes', action='store_true', help='Afficher les contrats non signés')
        parser.add_argument('--non_payes', action='store_true', help='Afficher les contrats non entièrement payés')

    def handle(self, *args, **kwargs):
        non_signes = kwargs['non_signes']
        non_payes = kwargs['non_payes']

        # Commencez par obtenir tous les contrats
        contrats = Contrat.objects.all()

        if non_signes:
            contrats = contrats.filter(contrat_signe=False)

        if non_payes:
            contrats = contrats.filter(montant_restant__gt=0)

        # Affichez les contrats qui correspondent aux conditions
        if contrats.exists():
            self.stdout.write(self.style.SUCCESS('Contrats correspondant aux conditions :'))
            for contrat in contrats:
                self.stdout.write(f'- ID : {contrat.id}')
                self.stdout.write(f'  Identifiant unique : {contrat.identifiant_unique}')
                self.stdout.write(f'  Client : {contrat.client}')
                self.stdout.write(f'  Montant total : {contrat.montant_total}')
                self.stdout.write(f'  Montant restant : {contrat.montant_restant}')
                self.stdout.write(f'  Contrat signé : {"Oui" if contrat.contrat_signe else "Non"}')
                self.stdout.write(f'  Contact commercial : {contrat.contact_commercial}')
                self.stdout.write(f'  Date de creation du contrat : {contrat.date_creation_contrat}')
                self.stdout.write('\n')
        else:
            self.stdout.write(self.style.SUCCESS('Aucun contrat ne correspond aux conditions spécifiées.'))
