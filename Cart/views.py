from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny


def get_or_create_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    current_session_cart, session_cart_created = Cart.objects.get_or_create(
        session_id=session_id,
        defaults={'user': None}
    )

    if request.user.is_authenticated:
        user_cart, user_cart_created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_id': None}
        )

        if not session_cart_created and current_session_cart.user is None and current_session_cart.id != user_cart.id:
            with transaction.atomic():
                for item in current_session_cart.cart_items.all().select_related('book'):
                    existing_user_item = CartItems.objects.filter(cart=user_cart, book=item.book).first()
                    if existing_user_item:
                        existing_user_item.quantity += item.quantity
                        existing_user_item.save()
                    else:
                        item.cart = user_cart
                        item.save()
                current_session_cart.delete()
            user_cart.refresh_from_db()
            return user_cart
        elif current_session_cart.id == user_cart.id and not current_session_cart.user:
            current_session_cart.user = request.user
            current_session_cart.session_id = None
            current_session_cart.save()
            return current_session_cart
        return user_cart
    else:
        return current_session_cart


class CartPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = get_or_create_cart(request)

        cart_for_serialization = Cart.objects.prefetch_related(
            'cart_items__book__authors',
            'cart_items__book__genre'
        ).select_related(
            'user'
        ).get(pk=cart.pk)

        if cart_for_serialization and cart_for_serialization.cart_items.exists():
            serializer = CartSerializer(instance=cart_for_serialization)
            return Response({'response': serializer.data}, status=status.HTTP_200_OK)
        return Response({'response': 'Your cart is empty!'}, status=status.HTTP_200_OK)


class AddCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, book_id):
        cart = get_or_create_cart(request)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        existing_item = CartItems.objects.filter(cart=cart, book=book).first()
        if existing_item:
            existing_item.quantity += 1
            existing_item.save()
            message = "Book quantity updated in cart successfully."
        else:
            CartItems.objects.create(cart=cart, book=book, quantity=1)
            message = "Book added to cart successfully."

        return Response({'message': message}, status=status.HTTP_201_CREATED)


class DeleteCartItemView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        cart = get_or_create_cart(request)
        try:
            cart_item = CartItems.objects.get(id=pk, cart=cart)
            cart_item.delete()
            return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CartItems.DoesNotExist:
            return Response({'error': 'Item not found in your cart.'}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        cart = get_or_create_cart(request)
        if cart and cart.cart_items.exists():
            cart.cart_items.all().delete()
            return Response({"message": "Cart items cleared successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Your cart is already empty."}, status=status.HTTP_200_OK)

































