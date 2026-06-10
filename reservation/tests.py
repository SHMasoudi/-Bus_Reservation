from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from transport.models import TransportCompany, Bus, Seat, Trip
from .models import Reservation, ReservationStatus
from rest_framework.test import APIClient


class ReservationModelTest(TestCase):

    def setUp(self):
        

        
        self.passenger = User.objects.create_user(
            phone_number='09123456789',
            gender='MALE'
        )

        
        self.owner = User.objects.create_user(
            phone_number='09111111111',
            role='TRANSPORT_OWNER'
        )

        
        self.company = TransportCompany.objects.create(
            owner=self.owner,
            name='شرکت تست'
        )
        self.bus = Bus.objects.create(
            company=self.company,
            plate_number='11A111',
            total_seats=10
        )
        self.seat = Seat.objects.create(
            bus=self.bus,
            seat_number=1,
            gender_type='MIXED'
        )
        self.trip = Trip.objects.create(
            bus=self.bus,
            origin_city='Tehran',
            destination_city='Isfahan',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=250000
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            seat=self.seat,
        )
        self.assertEqual(reservation.status, ReservationStatus.PENDING)

    def test_confirm_reservation(self):
        reservation = Reservation.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            seat=self.seat,
        )
        reservation.confirm()
        self.assertEqual(reservation.status, ReservationStatus.CONFIRMED)

    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            seat=self.seat,
        )
        reservation.cancel()
        self.assertEqual(reservation.status, ReservationStatus.CANCELLED)

    def test_cannot_confirm_cancelled_reservation(self):
        reservation = Reservation.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            seat=self.seat,
            status=ReservationStatus.CANCELLED
        )
        with self.assertRaises(ValueError):
            reservation.confirm()

    def test_expire_reservation(self):
        reservation = Reservation.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            seat=self.seat,
        )
        reservation.expire()
        self.assertEqual(reservation.status, ReservationStatus.EXPIRED)
        



class ReservationAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.passenger = User.objects.create_user(
            phone_number='09123456789',
            gender='MALE'
        )
        self.owner = User.objects.create_user(
            phone_number='09111111111',
            role='TRANSPORT_OWNER'
        )
        self.company = TransportCompany.objects.create(
            owner=self.owner,
            name='شرکت تست'
        )
        self.bus = Bus.objects.create(
            company=self.company,
            plate_number='11A111',
            total_seats=10
        )
        self.seat = Seat.objects.create(
            bus=self.bus,
            seat_number=1,
            gender_type='MIXED'
        )
        self.trip = Trip.objects.create(
            bus=self.bus,
            origin_city='Tehran',
            destination_city='Isfahan',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=250000
        )

    def test_create_reservation_authenticated(self):
        
        self.client.force_authenticate(user=self.passenger)

        response = self.client.post('/api/reservations/', {
            'trip': self.trip.id,
            'seat': self.seat.id,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'PENDING')

    def test_create_reservation_unauthenticated(self):
        
        response = self.client.post('/api/reservations/', {
            'trip': self.trip.id,
            'seat': self.seat.id,
        })

        self.assertEqual(response.status_code, 401)

    def test_passenger_sees_only_own_reservations(self):
        
        other_passenger = User.objects.create_user(
            phone_number='09999999999',
            gender='MALE'
        )
        other_seat = Seat.objects.create(
            bus=self.bus,
            seat_number=2,
            gender_type='MIXED'
        )

        
        Reservation.objects.create(
            passenger=other_passenger,
            trip=self.trip,
            seat=other_seat,
        )

       
        self.client.force_authenticate(user=self.passenger)
        response = self.client.get('/api/reservations/')

        
        self.assertEqual(len(response.data), 0)