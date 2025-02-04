from django.db import models
from django.utils.text import slugify
from Account.models import LibraryUsers
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db.models import Avg


class Author(models.Model):
    name = models.CharField(max_length=20)
    bio = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['id']),
        ]


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['id']),
        ]


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authors = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")
    price = models.PositiveIntegerField(default=0)
    offers = models.PositiveIntegerField(default=0)
    publication_date = models.DateField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="book_cover")
    pdf_file = models.FileField(
        upload_to='books_pdf/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        upload_to="books_audio/",
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])],
        null=True,
        blank=True
    )
    average_rating = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.title}"

    @property
    def new_price(self):
        return self.price - self.offers

    def update_average_rating(self):
        average = self.rating.aggregate(Avg('rate'))['rate__avg'] or 0.0
        self.average_rating = average
        self.save()

    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['-publication_date']),
        ]


class Comment(models.Model):
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]


class Rating(models.Model):
    RATE_CHOICE = (
        (1, 'very weak'),
        (2, 'weak'),
        (3, 'average'),
        (4, 'good'),
        (5, 'great'),
    )

    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="rating")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rating", blank=True, null=True)
    rate = models.PositiveIntegerField(
        choices=RATE_CHOICE, validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.rate}"


