from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
   profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

class Tache(models.Model):
    titre = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    dateDebut = models.DateTimeField(auto_now_add=True)
    dateFin = models.DateTimeField(auto_now=True)

    STATUTS = [
        ('A faire', 'À faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]
    PRIORITES = [
        ('Basse', 'Basse'),
        ('Moyenne', 'Moyenne'),
        ('Haute', 'Haute'),
    ]
    statut = models.CharField(max_length=10, choices=STATUTS, verbose_name='Statut')
    priorite = models.CharField(max_length=10, choices=PRIORITES, verbose_name='Priorité') 
    
   # def update_tache(self,titre,description):
        