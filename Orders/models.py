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
q



