from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from datetime import timedelta
from .models import User, OTPRequest
from transport.models import TransportCompany, Bus, Seat, Trip

class OTPRequestModelTest(TestCase):

    def test_otp_is_valid(self):
        
        otp = OTPRequest.objects.create(
            phone_number='09123456789',
            code='123456',
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        self.assertTrue(otp.is_valid())

    def test_otp_is_expired(self):
        
        otp = OTPRequest.objects.create(
            phone_number='09123456789',
            code='123456',
            expires_at=timezone.now() - timedelta(minutes=1)
        )
        self.assertFalse(otp.is_valid())

    def test_otp_is_already_used(self):
       
        otp = OTPRequest.objects.create(
            phone_number='09123456789',
            code='123456',
            is_verified=True,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        self.assertFalse(otp.is_valid())
        





class PermissionTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.passenger = User.objects.create_user(
            phone_number='09123456789',
            role='PASSENGER'
        )
        self.owner = User.objects.create_user(
            phone_number='09111111111',
            role='TRANSPORT_OWNER'
        )

    def test_passenger_cannot_create_company(self):
        
        self.client.force_authenticate(user=self.passenger)
        response = self.client.post('/api/transport/companies/', {
            'name': 'شرکت تست'
        })
        self.assertEqual(response.status_code, 403)

    def test_owner_can_create_company(self):
        
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/api/transport/companies/', {
            'name': 'شرکت تست'
        })
        self.assertEqual(response.status_code, 201)

    def test_owner_cannot_see_other_owners_company(self):
        
        other_owner = User.objects.create_user(
            phone_number='09222222222',
            role='TRANSPORT_OWNER'
        )
        TransportCompany.objects.create(owner=other_owner, name='شرکت دیگری')

        self.client.force_authenticate(user=self.owner)
        response = self.client.get('/api/transport/companies/')
        self.assertEqual(len(response.data), 0)