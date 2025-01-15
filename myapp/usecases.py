from django.db.models import QuerySet
from django.http import Http404
from opensearchpy.helpers.response import Response as OpenSearchQueryResponse

from .models import Article as ArticleModel
from .mappings import Article as ArticleMapping


def article_list() -> QuerySet["ArticleModel"]:
    qs = ArticleModel.objects.all()
    qs = qs.select_related("author")
    qs = qs.prefetch_related("tags")
    return qs


def article_detail(article_id: int) -> ArticleModel:
    qs = ArticleModel.objects.all()
    qs = qs.select_related("author")
    qs = qs.prefetch_related("tags")
    try:
        return qs.get(id=article_id)
    except ArticleModel.DoesNotExist:
        raise Http404(f"{article_id=} not found.")


def search_articles(q: str) -> OpenSearchQueryResponse:
    response = ArticleMapping.search_by_word(q)

    return response
