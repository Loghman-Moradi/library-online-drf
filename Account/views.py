import random
from django.contrib.messages import success
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LibraryUserSerializer
from rest_framework import generics
from .models import LibraryUsers
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from .kavenegar.KaveSms import send_sms_with_template
from rest_framework_simplejwt.tokens import RefreshToken


class SendOtpView(generics.GenericAPIView):
    serializer_class = LibraryUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            if not phone:
                return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

            code = ''.join(random.sample('0123456789', 6))
            tokens = {'token': code}
            expires_at = timezone.now() + timedelta(minutes=2)

            request.session['verification_code'] = code
            request.session['phone'] = phone
            request.session['expires_at'] = expires_at.isoformat()

            success = send_sms_with_template(phone, tokens, 'user-login')
            if success:
                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOtpView(generics.GenericAPIView):
    def post(self, request):
        received_code = request.data.get('code')
        verification_code = request.session.get('verification_code')
        phone = request.session.get('phone')
        expires_at = request.session.get('expires_at')

        if verification_code is None or phone is None or expires_at is None:
            return Response({'error': 'Session data missing'}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > timezone.datetime.fromisoformat(expires_at):
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        if received_code == verification_code:
            user = LibraryUsers.objects.filter(phone=phone).first()
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({
                    "message": "User found",
                    'user': user.phone,
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                characters = 'QWERTYUIOPASDFGHJKLZXCVBNM-0123456789-@_qwertyuiopasdfghjklzxcvbnm'
                user_password = ''.join(random.sample(characters, 8))
                user = LibraryUsers.objects.create_user(phone=phone)
                user.set_password(user_password)
                user.save()

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "User Created Successfully",
                    'user': user.phone,
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        user = request.user
        if user is None:
            return Response({"error": "The user is not authenticated."}, status=401)

        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Refresh token has expired. Please log in again using OTP."}, status=status.HTTP_401_UNAUTHORIZED)





# {
#     "message": "User found",
#     "user": "09214249950",

#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODU2Nzk5NSwiaWF0IjoxNzM4NDgxNTk1LCJqdGkiOiJiYzU2MTYxM2E4Nzc0MmJkYWJjYTg5NTE1NTE5MzEyZSIsInVzZXJfaWQiOjF9.dhmlnDq-N1tncCv8_d5FIAknLyqAWwRdRdvTNn5YiaE"
# }



# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4NDgzNzU4LCJpYXQiOjE3Mzg0ODE1OTUsImp0aSI6IjNkNmY4YTAxOGY0NzRjMzY5NGYxYjMxNTE0Y2RiODE2IiwidXNlcl9pZCI6MX0.m_f7Muf0jpjSXxaGrk0d4YjcIkWgZ7htt2FPPtlyFwg"
# }



