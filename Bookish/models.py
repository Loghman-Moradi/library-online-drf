from django.db import models
from django.utils.text import slugify


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



















