from rest_framework import serializers
from dives.models import Dive

class DiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dive
        fields = '__all__'
        