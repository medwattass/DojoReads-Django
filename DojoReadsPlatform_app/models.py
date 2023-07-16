from django.db import models
from log_reg_app.models import User


class AuthorManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['author_new']) < 2:
            errors["author_new"] = "The Author's name should be at least 2 characters"
        return errors


class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()


class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if Book.objects.filter(title=postData['title']).exists():
            errors["title"] = "This title have been already used"
        if len(postData['title']) < 2:
            errors["title_2"] = "The title should be at least 2 characters"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class ReviewManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 5:
            errors["content"] = "The review should be at least 5 characters"
        return errors


class Review(models.Model):
    content = models.TextField()
    rate = models.IntegerField()
    user = models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

