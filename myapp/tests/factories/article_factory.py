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
        if random.random() > 0.5:
            # Include "Python" in title
            return "This is awesome Python blog."
        else:
            # return factory.Faker("sentence", nb_words=4)
            return fake.sentence(nb_words=4)

    @factory.lazy_attribute
    def content(self):
        number_of_words = random.randint(50, 80)

        if random.random() > 0.5:
            # Include "python" in content
            words = fake.words(nb=number_of_words)
            words.insert(random.randint(0, number_of_words), "python")
            return " ".join(words)
        else:
            return fake.text(max_nb_chars=number_of_words)
