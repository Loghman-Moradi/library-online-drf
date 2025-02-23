from django.utils import timezone
from django.db import models
from Account.models import LibraryUsers
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


class Order(models.Model):
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="orders")
    coupon_used = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    subtotal = models.PositiveSmallIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    def calculate_subtotal(self):
        total = sum(item.final_price for item in self.order_items.all())
        total = int(total)

        if self.coupon_used and self.coupon:
            if (self.coupon.is_enable and
                    self.coupon.users_used.count() < self.coupon.max_usage and
                    self.coupon.active < timezone.now() < self.coupon.expire and
                    self.coupon.min_price <= total <= self.coupon.max_price):
                discount_amount = (total * self.coupon.discount_percentage) // 100
                total -= discount_amount

        self.subtotal = total
        print(f"Subtotal before save: {self.subtotal}")
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def final_price(self):
        return self.book.new_price
