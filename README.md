# Projet 12 :Développez une architecture back-end sécurisée avec Python et SQL


***

### ***Contexte :***
Epic Events est une entreprise qui organise des événements (fêtes,
réunions professionnelles, manifestations hors les murs) pour ses clients.
Nous souhaitons développer un logiciel CRM (Customer Relationship
Management) pour améliorer notre travail.
Le logiciel CRM permet de collecter et de traiter les données des clients
et de leurs événements, tout en facilitant la communication entre les
différents pôles de l'entreprise.
***
### ***Technologies :***
- Python
- Django
- Sqlite
- Pyjwt
- Sentry-sdk
***
### ***Installation :***

 - Télécharger le projet depuis [Github](https://github.com/CharkaouiSalwa/Projet_12.git)
 - Se positionner dans le dossier git téléchargé
 - Créer un environnement virtuel :
```
python -m venv env
```
 - Activer l'environnement virtuel : 
```
source  venv/bin/activate
```
 - Installer les bibliothéques nécessaires depuis le fichier requirements.txt :
``` shell
pip install -r requirements.txt
```
***
### ***Initialisation de la base de données :***
- Accédez au dossier de travail.
```
cd project
```
- Procédez à une recherche de migrations.
```
python manage.py makemigrations
```
- Lancer les migrations nécessaires.
```
python manage.py migrate
```
***
### ***Utilisation :***
- Démarrage du serveur local Accédez et au dossier de travail.
```
cd project
```
- Executer la commande pour creer un utilisateur.
```
python manage.py sign_up
```
- Ou bien generer le token directement et se connecter avec le user et mot de passe et enregistrer le token dans un fichie token.txt.
```
python manage.py login <user> <password> --file token.txt
```
- Apres vous pouvez commencer à exécuter les autres commande de la méme maniére.
- Executer la commande pour se déconecté et supprimer lo token du fichier.
```
python manage.py logout
```


<br/><br/><br/>
*Par Salwa CHARKAOUI* 