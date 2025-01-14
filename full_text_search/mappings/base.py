from opensearchpy import Document

from ..utils.opensearch_client import init_opensearch_client


class BaseDocument(Document):
    class Index:
        name: str

    client = init_opensearch_client()
    index_versioning_delimiter = "_"

    @classmethod
    def prepare_index(cls, version: int):
        """Init index with version, and set the alias for created index."""
        index_name = cls.Index.name + cls.index_versioning_delimiter + f"v{version}"
        cls.init(index=index_name, using=cls.client)

        actions = [
            {
                "add": {
                    "index": index_name,
                    "alias": cls.Index.name,
                }
            },
        ]
        cls.client.indices.update_aliases(body={"actions": actions})
