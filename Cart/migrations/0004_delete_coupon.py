# Generated by Django 5.1.5 on 2025-02-21 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_rename_mac_price_coupon_max_price'),
        ('Orders', '0004_coupon_alter_order_coupon'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
