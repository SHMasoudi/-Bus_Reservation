from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'trip', 'seat', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']