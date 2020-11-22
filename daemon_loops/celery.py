import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TwitterStorm.settings')
app = Celery('TwitterStormCeleryApp')
app.config_from_object('django.conf:settings')

# Va chercher dans tous les packages (ou apps-django, ou dossiers) un attribut (fichier) tasks.py
# pour y trouver les tâches
app.autodiscover_tasks()

# Si les tâches utilisent la machinerie de Django (ex: les modèles pour la BDD),
# alors ne pas définir les tâches dans ce fichier, sinon Celery n'a pas
# le temps de charger les modules Django
