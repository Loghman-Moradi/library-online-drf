from rest_framework import status
from rest_framework.response import Response
from Cart.models import CartItems
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class OrderPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user).first()
        if order is None:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = CartItems.objects.filter(cart__user=request.user)

        if not cart_items.exists():
            return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
            )
        cart_items.delete()
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            order.delete()
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Your order deleted successfully"}, status=status.HTTP_200_OK)













