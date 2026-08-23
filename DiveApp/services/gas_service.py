from gases.models import GasMixture
from django.core.exceptions import ValidationError

def validation_gas_mixture(oxygen_percentage, nitrogen_percentage):
    if oxygen_percentage < 0 or nitrogen_percentage < 0:
        raise ValidationError("Oxygen and nitrogen percentages must be non-negative.")
    if round(oxygen_percentage + nitrogen_percentage ,6) != 100.0:
        raise ValidationError("The sum of oxygen and nitrogen percentages must be 100.")
    
def create_gas_mixture(name,oxygen_percentage ,nitrogen_percentage):
    validation_gas_mixture(oxygen_percentage, nitrogen_percentage)
    gas_mixture = GasMixture(name=name, oxygen_percentage=oxygen_percentage, nitrogen_percentage=nitrogen_percentage)
    gas_mixture.save()
    return gas_mixture

def get_gas_mixture(mixture_id):
    try:
        return GasMixture.objects.get(id=mixture_id)
    except GasMixture.DoesNotExist:
        raise ValidationError(f"Gas mixture with id {mixture_id} does not exist.")


def update_gas_mixture(mixture_id, name=None, oxygen_percentage=None, nitrogen_percentage=None):
    gas_mixture = get_gas_mixture(mixture_id)
    
    if name is not None:
        gas_mixture.name = name
    if oxygen_percentage is not None:
        gas_mixture.oxygen_percentage = oxygen_percentage
    if nitrogen_percentage is not None:
        gas_mixture.nitrogen_percentage = nitrogen_percentage

    validation_gas_mixture(gas_mixture.oxygen_percentage, gas_mixture.nitrogen_percentage)
    gas_mixture.save()
    return gas_mixture

def delete_gas_mixture(mixture_id):
    gas_mixture = get_gas_mixture(mixture_id)
    gas_mixture.delete()

def list_gas_mixtures():
    return GasMixture.objects.all().order_by('name')


