from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status


def getCart(request, page_view=None):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    if page_view is True:
        session_id_from_request = (
            request.GET.get('session_id') or request.POST.get('session_id')
        )

        try:
            if session_id_from_request:
                cart = Cart.objects.get(session_id=session_id_from_request)
            else:
                cart = Cart.objects.get(user=request.user)
            return cart

        except Cart.DoesNotExist:
            return None

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart, session_id


class CartPageView(APIView):
    def get(self, request):
        cart = getCart(request, page_view=True)

        if cart:
            serializer = CartSerializer(instance=cart, many=False)
            return Response({"response": serializer.data}, status=status.HTTP_200_OK)
        return Response({"response": 'Your cart is empty!'}, status=status.HTTP_200_OK)











