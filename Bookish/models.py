from django.db import models
from django.utils.text import slugify
from Account.models import LibraryUsers
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Genre(models.Model):
    class Genres(models.TextChoices):
        Fiction = "Fiction"
        Romance = "Romance"
        Adventure = "Adventure"
        History = "History"
        Self_Help = "Self-Help"
        Business = "Business"
        Biography = "Biography"

    name = models.CharField(max_length=50, choices=Genres.choices, default=Genres.Fiction)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")
    price = models.PositiveIntegerField(default=0)
    offers = models.PositiveIntegerField(default=0)
    publication_date = models.DateField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="book_cover")
    file = models.FileField(upload_to='book_file')

    def __str__(self):
        return f"{self.title}"

    @property
    def new_price(self):
        return self.price - (self.price * self.offers / 100)


class Comment(models.Model):
    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.user}"


class Rating(models.Model):
    RATE_CHOICE = (
        (1, '1', 'very weak'),
        (2, '2', 'weak'),
        (3, '3', 'average'),
        (4, '4', 'good'),
        (5, '5', 'great'),
    )

    user = models.ForeignKey(LibraryUsers, on_delete=models.CASCADE, related_name="rating")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rating", blank=True, null=True)
    rate = models.PositiveIntegerField(
        choices=RATE_CHOICE, validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.rate}"





