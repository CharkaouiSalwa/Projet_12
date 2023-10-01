
from django import forms
from .models import UtilisateurPersonnalise


class InscriptionForm(forms.ModelForm):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UtilisateurPersonnalise
        fields = ['username', 'email', 'password']
