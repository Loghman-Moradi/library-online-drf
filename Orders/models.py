from django.utils import timezone
from rest_framework.exceptions import ValidationError

from Bookish.models import *


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True)
    min_price = models.PositiveSmallIntegerField()
    max_price = models.PositiveSmallIntegerField()
    discount_percentage = models.FloatField()
    active = models.DateTimeField(default=timezone.now)
    expire = models.DateTimeField()
    max_usage = models.PositiveSmallIntegerField(default=1)
    users_used = models.ManyToManyField(LibraryUsers, related_name='coupon_used', blank=True)
    is_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - Enable: {self.is_enable} - Discount %: {self.discount_percentage}"

    def used_time(self):
        return self.users_used.count()

    def clean(self):
        if self.min_price > self.max_price:
            raise ValidationError('Min price cannot be greater than max price.')
        if self.expire and self.active and self.expire < self.active:
            raise ValidationError('Expiration date cannot be before active date.')
        if not (0 <= self.discount_percentage and self.discount_percentage <= 100):
            raise ValidationError('Discount percentage must be between 0 and 100.')


class Order(models.Model):
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="orders")
    coupon_used = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    subtotal = models.PositiveSmallIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_subtotal(self):
        base_total = sum(item.final_price for item in self.order_items.all())
        final_total = base_total

        if self.coupon_used and self.coupon:
            coupon_obj = self.coupon

            is_coupon_valid = (
                    coupon_obj.is_enable and
                    coupon_obj.active < timezone.now() < coupon_obj.expire and
                    coupon_obj.min_price <= base_total <= coupon_obj.max_price
            )

            if is_coupon_valid:
                if coupon_obj.used_time() >= coupon_obj.max_usage:
                    self.coupon_used = False
                    self.coupon = None
                else:
                    discount_amount = (base_total * coupon_obj.discount_percentage) / 100
                    final_total -= discount_amount
            else:
                self.coupon_used = False
                self.coupon = None

        self.subtotal = max(0, final_total)

    def __str__(self):
        return f"Order {self.id} buy {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'book')

    def __str__(self):
        return f"{self.book.title} x {self.quantity} for Order {self.order.id}"

    @property
    def final_price(self):
        return self.book.new_price * self.quantity

    def clean(self):
        if self.quantity <= 0:
            raise models.ValidationError('Quantity must be a positive integer.')















