from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import TransportCompany, Bus, Seat, Trip
from accounts.permissions import IsTransportOwner
from .serializers import TransportCompanySerializer, BusSerializer, SeatSerializer, TripSerializer
from django.core.cache import cache
from rest_framework.response import Response
# Create your views here.


class TransportCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = TransportCompanySerializer
    permission_classes = [IsTransportOwner]

    def get_queryset(self):
        
        return TransportCompany.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)


class BusViewSet(viewsets.ModelViewSet):
    serializer_class = BusSerializer
    permission_classes = [IsTransportOwner]

    def get_queryset(self):
        
        return Bus.objects.filter(company__owner=self.request.user)


class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    permission_classes = [IsTransportOwner]

    def get_queryset(self):
        return Seat.objects.filter(bus__company__owner=self.request.user)


# class TripViewSet(viewsets.ModelViewSet):
#     serializer_class = TripSerializer
#     permission_classes = [AllowAny]  

#     def get_queryset(self):
#         queryset = Trip.objects.filter(is_active=True)

        
#         origin = self.request.query_params.get('origin')
#         destination = self.request.query_params.get('destination')

#         if origin:
#             queryset = queryset.filter(origin_city=origin)
#         if destination:
#             queryset = queryset.filter(destination_city=destination)

#         return queryset

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTransportOwner()]
        return [AllowAny()]
    
    def get_queryset(self):
        return Trip.objects.filter(is_active=True)
    
    def list(self, request):
        origin = request.query_params.get('origin', '')
        destination = request.query_params.get('destination', '')

        cache_key = f'trips_{origin}_{destination}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        queryset = self.get_queryset()

        if origin:
            queryset = queryset.filter(origin_city=origin)

        if destination:
            queryset = queryset.filter(destination_city=destination)

        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=300)

        return Response(serializer.data)