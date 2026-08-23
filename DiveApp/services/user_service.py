import hashlib
import os

from dives.models import Dive
from users.models import CertificationLevel, User
from django.core.exceptions import ValidationError



class UserService:
    @staticmethod
    def hash_password(password):
        salt = os.urandom(16).hex()   #une chaine de 32 caractères hexadécimaux représentant 16 octets aléatoires
        hash =hashlib.sha256(salt + password.encode()).hexdigest()  
        stored = f"{salt}${hash}"
        return stored
    @staticmethod
    def verify_password(stored, password):
        salt ,hash = stored.split('$')
        hash_new = hashlib.sha256((salt + password).encode()).hexdigest()  
        return hash_new == hash

    @staticmethod
    def create_user(user_data):
        user = User.objects.create(
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            email=user_data['email'],
            password=UserService.hash_password(user_data['password']),
            certification_level=user_data['certification_level'],
        )
        return user

    @staticmethod
    def get_user_by_email(us_email):
        try:
            user = User.objects.get(email=us_email)
            return user
        except User.DoesNotExist:
            raise ValidationError(f"User with email {us_email} does not exist.")
    
    @staticmethod
    def get_user_by_id(us_id):
        try:
            user = User.objects.get(id=us_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(f"User with id {us_id} does not exist.")
    

    @staticmethod
    def update_user(user_id, updated_data):
        try:
            user =UserService.get_user_by_id(user_id)
            for key,value in updated_data.items():
                if key == 'password':
                    user.password = UserService.hash_password(value)
                elif key == 'email':
                    if User.objects.filter(email=value).exclude(id=user_id).exists():
                        raise ValidationError(f"Email {value} is already in use.")
                    user.email = value
                elif key == 'certification_level':
                    if value not in [ch[0] for ch in CertificationLevel.choices]:
                        raise ValidationError(f"Invalid certification level: {value}.")
                    user.certification_level = value

                else:
                    setattr(user, key, value)
            user.save()
            return user
                
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")
        
    @staticmethod
    def delete_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            user.delete()
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")
        
    @staticmethod
    def register_user(user_data):
        if User.objects.filter(email=user_data['email']).exists():
            raise ValidationError(f"Email {user_data['email']} is already in use.")
        user = UserService.create_user(user_data)
        return user
    
    @staticmethod
    def login_user(email,password):
        try:
            user = UserService.get_user_by_email(email)
            if UserService.verify_password(user.password,password):
                return user
            else:
                raise ValidationError(f"User with email {email} does not exist or invalid password.")
        except User.DoesNotExist:
            raise ValidationError(f"User with email {email} does not exist or invalid password.")
    
    @staticmethod
    def logout_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            
            return True
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")
        
    @staticmethod
    def get_user_Profile(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            profile = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "certification_level": user.certification_level,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            return profile
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")
        
    @staticmethod
    def get_user_Dive_history(user_id):
        try:
            user =UserService.get_user_by_id(user_id)
            dive_history =Dive.objects.filter(user=user).order_by('-date') 
            return dive_history
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")
    