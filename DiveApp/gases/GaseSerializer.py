from rest_framework import serializers
from gases.models import GasMixture

class GasMixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasMixture
        fields = '__all__'