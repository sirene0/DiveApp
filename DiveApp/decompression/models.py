from django.db import models
from dives.models import Dive

# Create your models here.
class DecompressionModel(models.Model):
    dive = models.ForeignKey(Dive, on_delete=models.CASCADE, related_name='decompression_models')
    
    name = models.CharField(max_length=100)
    depth = models.FloatField(help_text="Depth in meters")
    duration = models.FloatField(help_text="Duration in minutes")
    order_number = models.IntegerField(help_text="Order number for sorting")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for Dive on {self.dive.date} at {self.dive.location}"