from django.db import models

# Create your models here.

from django.conf import settings


class TransportCompany(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='companies'
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Bus(models.Model):
    company = models.ForeignKey(
        TransportCompany,
        on_delete=models.CASCADE,
        related_name='buses'
    )
    plate_number = models.CharField(max_length=20, unique=True)
    total_seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plate_number
    

class SeatGenderType(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    MIXED = 'MIXED'



class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveIntegerField()
    gender_type = models.CharField(
        max_length=10,
        choices=SeatGenderType.choices,
        default=SeatGenderType.MIXED
    )
    is_reservable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('bus', 'seat_number')

    def __str__(self):
        return f'Bus {self.bus.plate_number} - Seat {self.seat_number}'
    
    

class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name='trips')
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.origin_city} to {self.destination_city}'