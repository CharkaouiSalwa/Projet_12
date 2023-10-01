from authentication.form import InscriptionForm
from django.shortcuts import render, redirect
from authentication.form import InscriptionForm
from django.contrib import messages

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre compte a été créé avec succès. Connectez-vous maintenant.')
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'authentication/inscription.html', {'form': form})


