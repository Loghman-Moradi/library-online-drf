import random
from django.contrib.messages import success
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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









# {
#     "message": "User Created Successfully",
#     "user": "09184517699",
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4NDA3NTg5LCJpYXQiOjE3Mzg0MDcyODksImp0aSI6ImI0NTVmYTAxMGYzYTQwYzk5YjMxMWU2OGVkMzFmYTk1IiwidXNlcl9pZCI6NX0.TYebGOHF5KzvtPsukbB4GbtLtJAyG14CacFXeJIHico",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODQ5MzY4OSwiaWF0IjoxNzM4NDA3Mjg5LCJqdGkiOiI5ZDgzYjZjZGMzZjc0YWY5OWY5ZjYyNjc1ZGJlNWM1NyIsInVzZXJfaWQiOjV9.Rl2IF0Rtl4md2KZue1_zIqZggsMvc2Jg4gbDor7Amxg"
# }








