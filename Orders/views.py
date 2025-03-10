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
        order.calculate_subtotal()
        cart_items.delete()

        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=code, is_enable=True)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code'}, status=status.HTTP_400_BAD_REQUEST)

        if coupon.expire < timezone.now():
            return Response({'error': 'Coupon has expired'}, status=status.HTTP_400_BAD_REQUEST)

        if coupon.users_used.count() >= coupon.max_usage:
            return Response({'error': 'Coupon usage limit reached'}, status=status.HTTP_400_BAD_REQUEST)

        if not (coupon.min_price <= order.subtotal <= (coupon.max_price or float('inf'))):
            return Response({'error': 'Order total does not meet coupon requirements'},
                            status=status.HTTP_400_BAD_REQUEST)

        discount_amount = (order.subtotal / 100) * coupon.discount_percentage
        order.subtotal -= discount_amount
        order.coupon_used = True
        order.coupon = coupon
        order.save()

        coupon.users_used.add(request.user)
        coupon.save()

        return Response({'message': 'Coupon applied successfully', 'discount': discount_amount},
                        status=status.HTTP_200_OK)

