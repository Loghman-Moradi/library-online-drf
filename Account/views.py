import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import LibraryUserSerializer, ProfileSerializer
from rest_framework.generics import GenericAPIView
from .models import LibraryUsers, Profile
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from .kavenegar.KaveSms import send_sms_with_template
from rest_framework_simplejwt.tokens import RefreshToken


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class SendOtpView(GenericAPIView):
    serializer_class = LibraryUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        code = ''.join(random.sample('0123456789', 6))
        tokens = {'token': code}
        print(tokens)
        expires_at = timezone.now() + timedelta(minutes=2)

        request.session['verification_code'] = code
        request.session['phone'] = phone
        request.session['expires_at'] = expires_at.isoformat()

        success = send_sms_with_template(phone, tokens, 'user-login')
        if success:
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOtpView(GenericAPIView):
    def post(self, request):
        received_code = request.data.get('code')
        verification_code = request.session.get('verification_code')
        phone = request.session.get('phone')
        expires_at_str = request.session.get('expires_at')

        if verification_code is None or phone is None or expires_at_str is None:
            request.session.pop('verification_code', None)
            request.session.pop('phone', None)
            request.session.pop('expires_at', None)
            return Response({'error': 'Session data missing or expired. Please request a new OTP.'},
                            status=status.HTTP_400_BAD_REQUEST)

        expires_at = timezone.datetime.fromisoformat(expires_at_str)

        if timezone.now() > expires_at:
            request.session.pop('verification_code', None)
            request.session.pop('phone', None)
            request.session.pop('expires_at', None)
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        if received_code == verification_code:
            request.session.pop('verification_code', None)
            request.session.pop('phone', None)
            request.session.pop('expires_at', None)

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
                user = LibraryUsers.objects.create_user(phone=phone)
                user.save()

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "User Created Successfully",
                    'user_phone': user.phone,
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# class RefreshTokenView(APIView):
#     def post(self, request):
#         refresh_token = request.data.get('refresh_token')
#         if not refresh_token:
#             return Response({"error": "Refresh token is required."}, status=400)
#
#         try:
#             refresh = RefreshToken(refresh_token)
#             access_token = str(refresh.access_token)
#             return Response({"access_token": access_token}, status=status.HTTP_200_OK)
#
#         except TokenError as e:
#             return Response({"error": "Refresh token has expired. Please log in again using OTP."},
#                             status=status.HTTP_401_UNAUTHORIZED)
#
#
#




