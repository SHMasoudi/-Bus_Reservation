
import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTPRequest
from .serializers import OTPRequestSerializer, OTPVerifySerializer
import logging


logger = logging.getLogger(__name__)

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']

        
        code = str(random.randint(100000, 999999))

        
        OTPRequest.objects.create(
            phone_number=phone_number,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        
        print(f'OTP code for {phone_number}: {code}')
        logger.info(f"OTP code: {code}")
        
        return Response({'message': 'کد OTP ارسال شد'})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        
        otp = OTPRequest.objects.filter(
            phone_number=phone_number,
            code=code
        ).last()

        if not otp or not otp.is_valid():
            return Response(
                {'error': 'کد اشتباه یا منقضی شده'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        otp.is_verified = True
        otp.save()

        
        user, created = User.objects.get_or_create(phone_number=phone_number)

        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
