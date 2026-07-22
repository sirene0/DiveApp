from django.db import models
from users.models import User



# Create your models here.
class DiveStatus (models.TextChoices):
    PLANNED = 'PL', 'Planned'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'CO', 'Completed'
    CANCELLED = 'CA', 'Cancelled'

class Dive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dives')
    gas_mix = models.ForeignKey('gases.GasMixture', on_delete=models.CASCADE, related_name='dives')
    date = models.DateField()
    depth = models.FloatField()
    duration = models.IntegerField(help_text="Duration in minutes")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    location = models.CharField(max_length=255)
    ascent_speed = models.FloatField(help_text="Ascent speed in meters per minute")
    status = models.CharField(max_length=2, choices=DiveStatus.choices, default=DiveStatus.PLANNED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dive by {self.user.firstname} {self.user.lastname} on {self.date} at {self.location}"
