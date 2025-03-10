import json
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Orders.models import Order
from rest_framework.response import Response
from rest_framework import status


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.filter(user=request.user).first()
        if not order:
            return Response({"error": "No order found."}, status=status.HTTP_404_NOT_FOUND)

        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.subtotal,
            "callback_url": 'http://localhost:8080/payment/verify/',
            "description": 'Payment for order',
            "metadata": {
                # "mobile": request.user.phone_number,
                # "email": request.user.email
            }
        }

        if settings.SANDBOX:
            api = 'sandbox'
        else:
            api = 'www'

        ZP_API_REQUEST = f"https://{api}.zarinpal.com/pg/v4/payment/request.json"
        req_header = {"accept": "application/json", "content-type": "application/json"}

        try:
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
            response_data = req.json()

            if 'errors' in response_data and response_data['errors']:
                return Response({"error": response_data['errors']}, status=status.HTTP_400_BAD_REQUEST)

            authority = response_data['data']['authority']
            return Response({"authority": authority, "payment_url": f"https://{api}.zarinpal.com/pg/StartPay/{authority}"},
                           status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user).first()
        if not order:
            return Response({"error": "No order found."}, status=status.HTTP_404_NOT_FOUND)

        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')

        if t_status == 'OK':
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.subtotal,
                "authority": t_authority
            }

            if settings.SANDBOX:
                api = 'sandbox'
            else:
                api = 'www'

            ZP_API_VERIFY = f"https://{api}.zarinpal.com/pg/v4/payment/verify.json"
            req_header = {"accept": "application/json", "content-type": "application/json"}

            try:
                req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
                response_data = req.json()

                if 'errors' in response_data and response_data['errors']:
                    return Response({"error": response_data['errors']}, status=status.HTTP_400_BAD_REQUEST)

                t_status_code = response_data['data']['code']
                if t_status_code == 100:
                    order.is_paid = True
                    order.save()
                    return Response({"message": "Transaction success.", "ref_id": response_data['data']['ref_id']},
                                   status=status.HTTP_200_OK)
                elif t_status_code == 101:
                    return Response({"message": "Transaction submitted.", "status": response_data['data']['message']},
                                   status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Transaction failed.", "status": response_data['data']['message']},
                                   status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Transaction failed or canceled by user"}, status=status.HTTP_400_BAD_REQUEST)