"""Vector store index types."""


from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Protocol, Union, runtime_checkable

from pydantic import BaseModel

from llama_index.data_structs.node import Node

DEFAULT_PERSIST_DIR = "./storage"
DEFAULT_PERSIST_FNAME = "vector_store.json"


@dataclass
class NodeWithEmbedding:
    """Node with embedding.

    Args:
        node (Node): Node
        embedding (List[float]): Embedding

    """

    node: Node
    embedding: List[float]

    @property
    def id(self) -> str:
        return self.node.get_doc_id()

    @property
    def ref_doc_id(self) -> str:
        return self.node.ref_doc_id or "None"


@dataclass
class VectorStoreQueryResult:
    """Vector store query result."""

    nodes: Optional[List[Node]] = None
    similarities: Optional[List[float]] = None
    ids: Optional[List[str]] = None


class VectorStoreQueryMode(str, Enum):
    """Vector store query mode."""

    DEFAULT = "default"
    SPARSE = "sparse"
    HYBRID = "hybrid"

    # fit learners
    SVM = "svm"
    LOGISTIC_REGRESSION = "logistic_regression"
    LINEAR_REGRESSION = "linear_regression"


class ExactMatchFilter(BaseModel):
    """Exact match metadata filter for vector stores."""

    key: str
    value: Union[str, int, float]


class MetadataFilters(BaseModel):
    """Metadata filters for vector stores.

    Currently only supports exact match filters.
    TODO: support more advanced expressions.
    """

    filters: List[ExactMatchFilter]


@dataclass
class VectorStoreQuery:
    """Vector store query."""

    query_embedding: Optional[List[float]] = None
    similarity_top_k: int = 1
    doc_ids: Optional[List[str]] = None
    query_str: Optional[str] = None

    mode: VectorStoreQueryMode = VectorStoreQueryMode.DEFAULT

    # NOTE: only for hybrid search (0 for bm25, 1 for vector search)
    alpha: Optional[float] = None

    # metadata filters
    filters: Optional[MetadataFilters] = None


@runtime_checkable
class VectorStore(Protocol):
    """Abstract vector store protocol."""

    stores_text: bool
    is_embedding_query: bool = True

    @property
    def client(self) -> Any:
        """Get client."""
        ...

    def add(
        self,
        embedding_results: List[NodeWithEmbedding],
    ) -> List[str]:
        """Add embedding results to vector store."""
        ...

    def delete(self, doc_id: str, **delete_kwargs: Any) -> None:
        """Delete doc."""
        ...

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        """Query vector store."""
        ...

    def persist(self, persist_path: str) -> None:
        return None
