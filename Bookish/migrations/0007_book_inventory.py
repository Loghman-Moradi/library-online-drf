# Generated by Django 5.1.5 on 2025-02-08 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookish', '0006_book_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='inventory',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
