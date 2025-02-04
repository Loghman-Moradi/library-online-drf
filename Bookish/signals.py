from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Bookish.models import Rating, Book


@receiver(post_save, sender=Rating)
def update_book_average(sender, instance, **kwargs):
        instance.book.update_average_rating()


@receiver(post_delete, sender=Rating)
def delete_book_average(sender, instance, **kwargs):
    instance.book.update_average_rating()


