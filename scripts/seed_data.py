import random

from tqdm import tqdm
from faker import Faker
from django.core.management import call_command
from opensearchpy import helpers

from myapp.models import Article, ArticleTag
from myapp.tests.factories import ArticleFactory, UserFactory
from myapp.mappings import Article as ArticleDocument
from full_text_search.utils.opensearch_client import init_opensearch_client

call_command("flush", interactive=False)
ArticleDocument.client.indices.delete(
    ArticleDocument.index_alias_name + "_v1", ignore=404
)
ArticleDocument.prepare_index(version=1)

random.seed(42)
Faker.seed(42)

user = UserFactory.create()
python_tag, _ = ArticleTag.objects.get_or_create(slug="python", display_name="Python")

ARTICLES_COUNT = 200
for _ in tqdm(range(ARTICLES_COUNT)):
    # --- Create Article objects in RDS
    a = ArticleFactory.create(author=user)
    if "python" in a.content:
        a.tags.add(python_tag)


# --- Indexing: create documents into OpenSearch
client = init_opensearch_client()
qs = Article.objects.all().prefetch_related("tags")

actions = [
    ArticleDocument(
        id=article.id,
        title=article.title,
        content=article.content,
        tags=[{"slug": tag.slug} for tag in article.tags.all()],
    ).to_dict(include_meta=True)
    for article in tqdm(qs)
]

success, _ = helpers.bulk(client, actions)

print("###", qs.count())
