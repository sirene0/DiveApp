from alerts.models import Alert, AlertSeverity
from users.models import User
from dives.models import Dive

from django.core.exceptions import ValidationError
DEPTH_LIMIT   = { 'P1': 20, 'P2': 40,'P3': 60 }



@staticmethod
def generate_alerts(dive, title, message, severity):
    alert = Alert.objects.create(
        dive=dive,
        title=title,
        message=message,
        severity=severity
    )
    return alert


@staticmethod
def list_alerts(dive_ID):
    return Alert.objects.filter(dive_id=dive_ID).order_by('-created_at')


@staticmethod
def check_depth_limit(dive_ID):
    try:
        dive = Dive.objects.get(id=dive_ID)
        if dive.user.certification_level in DEPTH_LIMIT and dive.depth > DEPTH_LIMIT[dive.user.certification_level]:
            generate_alerts(
                dive=dive,
                title='Depth Limit Exceeded',
                message=f'Dive depth of {dive.depth} meters exceeds the limit for certification level {dive.user.certification_level}.',
                severity=AlertSeverity.DANGER
            )
        
    except Dive.DoesNotExist:
        raise ValidationError(f"Dive with id {dive_ID} does not exist.")
    
        
    

    
@staticmethod
def check_duration_limit(dive_ID):
    try:
        dive = Dive.objects.get(id=dive_ID)
        if  dive.duration > 60:
            generate_alerts(
                dive=dive,
                title='Duration Limit Exceeded',
                message=f'Dive duration of {dive.duration} minutes exceeds the limit for every certification level.',
                severity=AlertSeverity.DANGER
            )
        
    except Dive.DoesNotExist:
        raise ValidationError(f"Dive with id {dive_ID} does not exist.")

@staticmethod
def check_Ascent_Speed(dive_ID):
    try:
        dive = Dive.objects.get(id=dive_ID)
        if dive.ascent_Speed > 9:
            generate_alerts(
                dive=dive,
                title='Ascent Speed Limit Exceeded',
                message=f'Dive ascent speed of {dive.ascent_Speed} meters per minute exceeds the limit for every certification level.',
                severity=AlertSeverity.DANGER
            )
        
    except Dive.DoesNotExist:
        raise ValidationError(f"Dive with id {dive_ID} does not exist.")

