import random

from tqdm import tqdm
from faker import Faker
from django.core.management import call_command
from opensearchpy import helpers

from myapp.models import Article, ArticleTag
from myapp.tests.factories import ArticleFactory, UserFactory
from myapp.mappings import Article as ArticleDocument
from full_text_search.utils.opensearch_client import init_opensearch_client

# Erase all data
call_command("flush", interactive=False)
ArticleDocument.client.indices.delete(ArticleDocument.Index.name + "_v1", ignore=404)
ArticleDocument.prepare_index(version=1)

# Fix random seed
random.seed(42)
Faker.seed(42)

# --- Create objects into RDS
user = UserFactory.create()
python_tag, _ = ArticleTag.objects.get_or_create(slug="python", display_name="Python")
ruby_tag, _ = ArticleTag.objects.get_or_create(slug="ruby", display_name="Ruby")

study_tag, _ = ArticleTag.objects.get_or_create(slug="study", display_name="Study")
diary_tag, _ = ArticleTag.objects.get_or_create(slug="diary", display_name="Diary")

ARTICLES_COUNT = 200
for _ in tqdm(range(ARTICLES_COUNT)):
    a = ArticleFactory.create(author=user)

    tag_choices = [python_tag, ruby_tag, study_tag, diary_tag]
    tags_to_add = random.choices(tag_choices, k=random.randint(0, len(tag_choices)))
    a.tags.add(*tags_to_add)

# --- Indexing: create documents into OpenSearch
client = init_opensearch_client()
qs = Article.objects.all().prefetch_related("tags")

actions = [
    ArticleDocument(
        id=article.id,
        title=article.title,
        content=article.content,
        tags=[
            {"display_name": tag.display_name, "slug": tag.slug}
            for tag in article.tags.all()
        ],
    ).to_dict(include_meta=True)
    for article in tqdm(qs)
]

success, _ = helpers.bulk(client, actions)
