from django.db import models

# Create your models here.
class AlertSeverity(models.TextChoices):
    INFO = 'INFO', 'Info'
    WARNING = 'WARNING', 'Warning'
    DANGER = 'DANGER', 'Danger'

class Alert (models.Model):
    dive = models.ForeignKey('dives.Dive', on_delete=models.CASCADE, related_name='alerts')
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=AlertSeverity.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity} - Dive #{self.dive.id}: {self.title}"