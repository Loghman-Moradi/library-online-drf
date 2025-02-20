from django.utils import timezone
from django.db import models
from Account.models import LibraryUsers
from Bookish.models import *
from Cart.models import Coupon


class Order(models.Model):
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="orders")
    coupon_used = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupon", null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    @property
    def subtotal(self):
        total = sum(item.final_price for item in self.order_items.all())

        if self.coupon_used is False:
            return total

        if not (self.coupon.is_enable and self.coupon.max_usage <= self.coupon.used_by):
            return total

        if not (self.coupon.active < timezone.now() < self.coupon.expire):
            return total

        if not (self.coupon.min_price <= total <= self.coupon.max_price):
            return total

        discount_amount = (total / 100) * self.coupon.discount_percentage
        return total - discount_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def final_price(self):
        return self.book.new_price * self.quantity
















