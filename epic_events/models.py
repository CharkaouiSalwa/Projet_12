from django.contrib.auth.models import AbstractUser
from django.db import models



class Client(models.Model):
    nom_complet = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    nom_entreprise = models.CharField(max_length=255)
    date_creation = models.DateField()
    derniere_mise_a_jour = models.DateTimeField()
    contact_commercial = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_complet


class Evenement(models.Model):
    event_id = models.CharField(max_length=20, unique=True)
    contrat = models.ManyToManyField('Contrat')
    nom_client = models.CharField(max_length=255)
    contact_client = models.CharField(max_length=255)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    contact_support = models.CharField(max_length=255)
    lieu = models.CharField(max_length=255)
    participants = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return self.event_id

class Contrat(models.Model):
    identifiant_unique = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    evenements = models.ManyToManyField(Evenement, related_name='Contrat')
    contact_commercial = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation_contrat = models.DateField()
    contrat_signe = models.BooleanField(default=False)

    def __str__(self):
        return self.identifiant_unique



class Collaborateur(AbstractUser):
    ROLE_CHOICES = (
        ('commercial', 'Commercial'),
        ('support', 'Support'),
        ('gestion', 'Gestion'),
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    # Identifiants de connexion
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    # Spécifiez le champ à utiliser comme nom d'utilisateur
    USERNAME_FIELD = 'username'
    # Spécifiez les champs requis lors de la création d'un utilisateur
    REQUIRED_FIELDS = ['email', 'telephone']

    def __str__(self):
        return self.username