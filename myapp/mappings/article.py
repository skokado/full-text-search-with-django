from typing import TYPE_CHECKING, Optional
from opensearchpy import InnerDoc
from opensearchpy.helpers.analysis import Analyzer
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
    display_name = field.Text()
    slug = field.Text(analyzer=keyword_lowercase_analyzer)


class Article(BaseDocument):
    class Index:
        name = "myapp_article"

    id = field.Integer()
    title = field.Text()
    content = field.Text()
    tags = field.Nested(ArticleTag)

    @classmethod
    def search_by_word(
        cls,
        word: str,
        boost: Optional[dict[str, float]] = None,
        offset: int = 0,
        size: int = 200,
        highlight: Optional[dict[str, dict]] = None,
    ) -> "Response":
        query = {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {"query": word} | {"boost": boost["title"]}
                            if boost and "title" in boost
                            else {"query": word}
                        }
                    },
                    {
                        "match": {
                            "content": {"query": word} | {"boost": boost["content"]}
                            if boost and "content" in boost
                            else {"query": word}
                        }
                    },
                    {
                        "nested": {
                            "path": "tags",
                            "query": {
                                "match": {
                                    "tags.slug": {"query": word}
                                    | {"boost": boost["tags.slug"]}
                                    if boost and "tags.slug" in boost
                                    else {"query": word}
                                }
                            },
                        }
                    },
                ]
            },
        }
        response = (
            cls.search(using=cls.client)
            .query(query)
            .extra(
                **{
                    "from": offset,
                    "size": size,
                }
            )
            .highlight(
                "title",
                "content",
                "tags.slug",
            )
            .execute()
        )
        return response
