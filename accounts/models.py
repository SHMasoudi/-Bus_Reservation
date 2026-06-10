from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.



class UserRole(models.TextChoices):
    ADMIN = 'ADMIN'
    TRANSPORT_OWNER = 'TRANSPORT_OWNER'
    PASSENGER = 'PASSENGER'


class Gender(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    
class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تلفن الزامیست')
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields['role'] = UserRole.ADMIN
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.PASSENGER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number
    
    
    





class OTPRequest(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OTP for {self.phone_number}'

    def is_valid(self):
        if self.is_verified:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True