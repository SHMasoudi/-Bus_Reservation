from rest_framework import serializers
from .models import TransportCompany,Trip,Bus,Seat

class TransportCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportCompany
        fields = ['id', 'name', 'is_active', 'created_at']


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'company', 'plate_number', 'total_seats', 'is_active']
        

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'bus', 'seat_number', 'gender_type', 'is_reservable']
        

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'bus', 'origin_city', 'destination_city', 'departure_datetime', 'price', 'is_active']