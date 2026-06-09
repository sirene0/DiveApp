from django.db import models

# Create your models here.
class GasMixture(models.Model):
    name = models.CharField(max_length=100)
    oxygen_percentage = models.FloatField(help_text="Oxygen percentage in the gas mixture")
    nitrogen_percentage = models.FloatField(help_text="Nitrogen percentage in the gas mixture")
    

    def __str__(self):
        return self.name