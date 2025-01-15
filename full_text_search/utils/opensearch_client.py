from functools import lru_cache

from opensearchpy import OpenSearch


@lru_cache(maxsize=1)
def init_opensearch_client(alias: str = "default") -> OpenSearch:
    return OpenSearch(
        alias=alias,
        hosts=[
            {"host": "localhost", "port": 9200}
        ],  # NOTE Recommended to use environment variables by settings.py
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
