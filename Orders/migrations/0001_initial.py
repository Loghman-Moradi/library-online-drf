# Generated by Django 5.1.5 on 2025-02-18 18:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Bookish', '0007_book_inventory'),
        ('Cart', '0003_rename_mac_price_coupon_max_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_used', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='Cart.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Bookish.book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Orders.order')),
            ],
        ),
    ]
