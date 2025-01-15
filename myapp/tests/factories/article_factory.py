from functools import lru_cache
import random

import factory
from factory.django import DjangoModelFactory
import faker

from myapp.models import Article, ArticleTag

from .user_factory import UserFactory


fake = faker.Faker()


@lru_cache(maxsize=1)
def get_words_list_include_python() -> list[str]:
    return ["python"] + fake.get_words_list()


class ArticleTagFactory(DjangoModelFactory):
    class Meta:
        model = ArticleTag
        django_get_or_create = ("slug",)

    display_name = factory.Faker("word")

    @factory.lazy_attribute
    def slug(self):
        return self.display_name.lower()


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def title(self):
        number_of_title_words = random.randint(5, 15)

        if random.random() > 0.5:
            # Include "Python" in title
            words = fake.words(number_of_title_words)
            words.insert(
                random.randint(0, number_of_title_words),
                random.choice(["Python", "python"]),
            )
            return " ".join(words) + "."
        else:
            return fake.sentence(nb_words=number_of_title_words)

    @factory.lazy_attribute
    def content(self):
        number_of_words = random.randint(100, 300)

        if random.random() > 0.5:
            # Include "python" in content
            words = fake.words(nb=number_of_words)
            words.insert(
                random.randint(0, number_of_words), random.choice(["Python", "python"])
            )
            return " ".join(words)
        else:
            return fake.text(max_nb_chars=number_of_words)
