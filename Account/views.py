import random
from .serializers import LibraryUserSerializer
from rest_framework import generics
from .models import LibraryUsers
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from .kavenegar.KaveSms import send_sms_with_template


class SendOtpView(generics.GenericAPIView):
    def post(self, request):
        serializer = LibraryUserSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
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
                return Response({"error": f"Failed to send OTP:"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            try:
                user = LibraryUsers.object.get(phone=phone)
                return Response({"message": "user found", 'user': user}, status=status.HTTP_200_OK)
            except LibraryUsers.DoesNotExist:
                characters = 'QWERTYUIOPASDFGHJKLZXCVBNM-0123456789-@_qwertyuiopasdfghjklzxcvbnm'
                user_password = ''.join(random.sample(characters, 8))
                user = LibraryUsers.object.create_user(phone=phone)
                user.set_password(user_password)
                user.save()
                return Response({"message": "User Created Successfully", 'phone': phone},
                                    status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)





















