# Generated by Django 5.1.5 on 2025-03-10 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_remove_libraryusers_first_name_and_more'),
        ('Bookish', '0008_bookpurchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='Bookish.book'),
        ),
    ]
