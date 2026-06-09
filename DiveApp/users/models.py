from django.db import models

# Create your models here.
class CertificationLevel(models.TextChoices):
    P1 = 'P1', 'P1'
    P2 = 'P2', 'P2'
    P3 = 'P3', 'P3'

class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    certification_level = models.CharField(max_length=2, choices=CertificationLevel.choices, default=CertificationLevel.P1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"