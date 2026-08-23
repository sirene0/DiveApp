from rest_framework import serializers
from decompression.models import DecompressionModel

class DecompressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecompressionModel
        fields = '__all__'
        