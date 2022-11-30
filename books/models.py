from account.models import CustomUser as User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    book_cover = models.ImageField(default='cover_book.png')

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    bio = models.TextField()
    born = models.CharField(max_length=120)
    residency = models.CharField(max_length=150, blank=True)
    motto = models.TextField(blank=True)
    author_image = models.ImageField(default='default_author.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.book.title} by {self.author.first_name}'


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} stars by {self.user.username} for '{self.book.title}'"

