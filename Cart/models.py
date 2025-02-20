from django.db import models
from Account.models import LibraryUsers
from Bookish.models import Book


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True,  verbose_name="ID")
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    session_id = models.CharField(max_length=60, unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.user) if self.user else self.session_id

    def total_price(self):
        total = 0
        for item in self.cart_items.all():
            total += item.subtotal()
        return total


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveSmallIntegerField(default=1)


    class Meta:
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.book.title} - {self.quantity}"

    def subtotal(self):
        return self.book.new_price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True)
    min_price = models.FloatField()
    max_price = models.FloatField()
    discount_percentage = models.FloatField()
    active = models.DateField()
    expire = models.DateField()
    max_usage = models.PositiveSmallIntegerField(default=1)
    used_by = models.ManyToManyField(LibraryUsers, related_name="coupon_used")
    is_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - Enable: {self.is_enable} - Discount %: {self.discount_percentage}"

    def used_time(self):
        return self.used_by.count()






















