from typing import TYPE_CHECKING

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)


class ArticleTag(models.Model):
    display_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)


class Article(models.Model):
    if TYPE_CHECKING:
        id: int

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = models.ManyToManyField(ArticleTag, related_name="articles")
