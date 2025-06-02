from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from Cart.models import CartItems
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class OrderPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).select_related(
            'user',
            'coupon'
        ).prefetch_related(
            'order_items__book__authors',
            'order_items__book__genre',
            'order_items'
        ).order_by('-created_at')

        if not orders.exists():
            return Response({'detail': 'No orders found for this user.'},
                            status=status.HTTP_200_OK)
        serializer = OrderSerializer(instance=orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = CartItems.objects.filter(cart__user=request.user).select_related('book')

        if not cart_items.exists():
            return Response({'error': 'Your cart is empty. Please add items before creating an order'},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            order_items_to_create = []
            for item in cart_items:
                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        book=item.book,
                        quantity=item.quantity,
                    )
                )
            OrderItem.objects.bulk_create(order_items_to_create)
            order.calculate_subtotal()
            order.save()
            cart_items.delete()

        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        order_id = request.data.get('order_id')

        if not code or not order_id:
            return Response({'error': 'Coupon code and order ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.prefetch_related('order_items__book').get(
                id=order_id, user=request.user, is_paid=False
            )
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or already paid.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.prefetch_related('users_used').get(code=code, is_enable=True)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code.'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()
        if coupon.expire < current_time:
            return Response({'error': 'Coupon has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        order.calculate_subtotal()

        if not (coupon.min_price <= order.subtotal <= coupon.max_price):
            return Response({
                'error': f'Order total ({order.subtotal}) does not meet coupon requirements (Min: {
                coupon.min_price}, Max: {coupon.max_price}).'},
                            status=status.HTTP_400_BAD_REQUEST)

        if coupon.users_used.filter(id=request.user.id).exists():
            return Response({'error': 'You have already used this coupon.'}, status=status.HTTP_400_BAD_REQUEST)

        if coupon.used_time() >= coupon.max_usage:
            return Response({'error': 'Coupon usage limit reached.'}, status=status.HTTP_400_BAD_REQUEST)

        order.coupon_used = True
        order.coupon = coupon
        order.calculate_subtotal()
        order.save(update_fields=['coupon_used', 'coupon', 'subtotal'])

        return Response({'message': 'Coupon applied successfully.', 'new_subtotal': order.subtotal},
                        status=status.HTTP_200_OK)


















