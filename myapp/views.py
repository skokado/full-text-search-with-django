from django.views.generic import TemplateView

from .models import Article
from . import usecases


class HomeView(TemplateView):
    """Article List"""

    template_name = "myapp/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        articles = usecases.article_list()
        ctx["articles"] = articles
        return ctx


class ArticleDetailView(TemplateView):
    """Article Detail"""

    template_name = "myapp/article_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["article"] = usecases.article_detail(kwargs["article_id"])
        return ctx


class ArticleSearchView(TemplateView):
    """Search Articles"""

    template_name = "myapp/search_result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        if not q:
            ctx["searched_articles"] = []
            return ctx

        ctx["query"] = q
        ctx["searched_articles"] = usecases.search_articles(q)
        return ctx
