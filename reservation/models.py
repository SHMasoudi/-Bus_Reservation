from django.db import models

# Create your models here.

from django.conf import settings
from transport.models import Trip, Seat


class ReservationStatus(models.TextChoices):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    

class Reservation(models.Model):
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reservations'
    )
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='reservations')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name='reservations')
    status = models.CharField(
        max_length=15,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reservation {self.id} - {self.passenger} - {self.status}'
    

    def confirm(self):
        if self.status != ReservationStatus.PENDING:
            raise ValueError('فقط رزرو PENDING قابل تایید است')
        self.status = ReservationStatus.CONFIRMED
        self.save()

    def cancel(self):
        if self.status == ReservationStatus.EXPIRED:
            raise ValueError('رزرو منقضی شده قابل لغو نیست')
        self.status = ReservationStatus.CANCELLED
        self.save()

    def expire(self):
        if self.status == ReservationStatus.PENDING:
            self.status = ReservationStatus.EXPIRED
            self.save()