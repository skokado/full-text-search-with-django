from typing import TYPE_CHECKING
from opensearchpy import InnerDoc
from opensearchpy.helpers import field
from opensearchpy.helpers.analysis import analyzer

from full_text_search.mappings import BaseDocument

if TYPE_CHECKING:
    from opensearchpy.helpers.response import Response


keyword_lowercase_analyzer = analyzer(
    "keyword_lowercase",
    tokenizer="keyword",
    filter=["lowercase"],
)


class ArticleTag(InnerDoc):
    slug = field.Text(analyzer=keyword_lowercase_analyzer)


class Article(BaseDocument):
    class Index:
        name = "myapp_article"

    id = field.Integer()
    title = field.Text()
    content = field.Text()
    tags = field.Nested(ArticleTag)

    @classmethod
    def search_by_word(cls, q: str) -> "Response":
        """
        Search target fields:
            - title (weight: 2)
            - content (weight: 1)
            - tags.slug (nested) (weight: 1)
        """
        query = {
            "bool": {
                "should": [
                    {"match": {"title": {"query": q, "boost": 2.0}}},
                    {"match": {"content": {"query": q, "boost": 1.0}}},
                    {
                        "nested": {
                            "path": "tags",
                            "query": {
                                "match": {"tags.slug": {"query": q, "boost": 1.0}}
                            },
                        }
                    },
                ]
            },
        }
        return (
            cls.search(using=cls.client)
            .query(query)
            .extra(
                size=300,
                highlight={
                    "fields": {
                        # Highlights the hitted words in the target fields
                        # defaults is quoted with <em> tag
                        "title": {},
                        "content": {},
                    }
                },
            )
            .execute()
        )
