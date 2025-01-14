import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "myapp.User"

    name = factory.Faker("name")
