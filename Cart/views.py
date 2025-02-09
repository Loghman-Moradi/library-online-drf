from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny


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
                if request.user.is_authenticated:
                    cart = Cart.objects.get(user=request.user)
                else:
                    cart = Cart.objects.get(session_id=session_id)
            return cart

        except Cart.DoesNotExist:
            return None

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart, session_id


class CartPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = getCart(request, page_view=True)

        if cart:
            serializer = CartSerializer(instance=cart, many=False)
            return Response({"response": serializer.data}, status=status.HTTP_200_OK)
        return Response({"response": 'Your cart is empty!'}, status=status.HTTP_200_OK)


class AddCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, book_id):
        cart, session_id = getCart(request)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
            elif quantity > book.inventory:
                return Response({"error": "The number is more than the stock."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItems.objects.get_or_create(cart=cart, book=book, defaults={'price': book.new_price})

        if not created:
            cart_item.quantity += quantity
            cart_item.price = book.new_price
            cart_item.save()

        return Response({'Messages': "Book added to cart successfully."}, status=status.HTTP_200_OK)


class UpdateCartView(APIView):
    def post(self, request, book_id):
        cart, session_id = getCart(request)

        try:
            cart_item = CartItems.objects.get(cart=cart, book__id=book_id)
        except CartItems.DoesNotExist:
            return Response({"error": 'item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity', None)
        if quantity is None:
            return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
            elif quantity > cart_item.book.inventory:
                 return Response({"error": "The number is more than the stock."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.price = cart_item.book.new_price
        cart_item.save()

        return Response({"message": "Cart updated successfully."}, status=status.HTTP_200_OK)


class DeleteCartView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            cart_item = CartItems.objects.get(id=pk)
            cart_item.delete()
            return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CartItems.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteWholeCart(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        cart, session_id = getCart(request)
        if cart:
            print(cart)
            print('session_id', session_id)
            cart.cart_items.all().delete()
            return Response(
                {"response": "Cart Items deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)





































































