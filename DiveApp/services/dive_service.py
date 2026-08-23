from dives.models import Dive
from django.core.exceptions import ValidationError


class DiveService:
    @staticmethod
    def create_dive(user, dive_data):
        dive = Dive.objects.create(
            user=user,
            date=dive_data['date'],
            location=dive_data['location'],
            depth=dive_data['depth'],
            duration=dive_data['duration'],
            temperature=dive_data['temperature'],
            ascent_Speed=dive_data['ascent_Speed'],
            gas_mix=dive_data['gas_mix'],
            status=Dive.DiveStatus.PLANNED
        )
        return dive
    
    @staticmethod
    def update_dive(user,dive_id ,dive_data):
        dive = DiveService.get_dive(user, dive_id)
        update_fields = [
            'date', 'location', 'depth', 'duration', 'temperature', 'ascent_Speed', 'gas_mix', 'status'
        ]
        for field in update_fields:
            if field in dive_data:
                setattr(dive, field, dive_data[field])
        dive.save()
        return dive
    
    @staticmethod
    def delete_dive(user,dive_id):
        dive = DiveService.get_dive(user, dive_id)
        dive.delete()
    
    @staticmethod
    def get_dive(user,dive_id):
        try:
            return Dive.objects.get(id=dive_id, user=user)
        except Dive.DoesNotExist:
            raise ValidationError(f"Dive with id {dive_id} does not exist for the user.")
        
    @staticmethod
    def list_user_dives(user):
        return Dive.objects.filter(user=user).order_by('-date')
    
    @staticmethod
    def start_dive(user, dive_id):
        dive = DiveService.get_dive(user, dive_id)
        if dive.status != Dive.DiveStatus.PLANNED:
                raise ValidationError("Only planned dives can be started.")
        dive.status = Dive.DiveStatus.IN_PROGRESS
        dive.save()
        return dive
    
    
    @staticmethod
    def finish_dive(user, dive_id):
        dive = DiveService.get_dive(user, dive_id)
        if dive.status != Dive.DiveStatus.IN_PROGRESS:
            raise ValidationError("Only in-progress dives can be completed")
        dive.status = Dive.DiveStatus.COMPLETED
        dive.save()
        
        return dive
    
    