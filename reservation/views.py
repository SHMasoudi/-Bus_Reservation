from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Reservation, ReservationStatus
from .serializers import ReservationSerializer
from transport.models import Seat, Trip
from accounts.permissions import IsPassenger

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsPassenger]

    def get_queryset(self):
        
        return Reservation.objects.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        trip = serializer.validated_data['trip']
        seat = serializer.validated_data['seat']
        passenger = self.request.user

       
        if not seat.is_reservable:
            raise ValueError('این صندلی قابل رزرو نیست')

       
        if seat.gender_type == 'MALE' and passenger.gender != 'MALE':
            raise ValueError('این صندلی مخصوص آقایان است')
        if seat.gender_type == 'FEMALE' and passenger.gender != 'FEMALE':
            raise ValueError('این صندلی مخصوص خانم‌ها است')

       
        already_reserved = Reservation.objects.filter(
            trip=trip,
            seat=seat,
            status__in=[ReservationStatus.PENDING, ReservationStatus.CONFIRMED]
        ).exists()

        if already_reserved:
            raise ValueError('این صندلی قبلاً رزرو شده')

        serializer.save(passenger=passenger)

    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation.cancel()
            return Response({'message': 'رزرو لغو شد'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation.confirm()
            return Response({'message': 'رزرو تایید شد'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        