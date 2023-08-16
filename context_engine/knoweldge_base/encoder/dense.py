from typing import List

from pinecone_text.dense.base_dense_ecoder import BaseDenseEncoder

from context_engine.knoweldge_base.encoder.base import Encoder
from context_engine.knoweldge_base.models import KBQuery, KBEncodedDocChunk, KBDocChunk
from context_engine.models.data_models import Query


class DenseEmbeddingsEncoder(Encoder):

    def __init__(self, dense_encoder: BaseDenseEncoder, **kwargs):
        super().__init__(**kwargs)
        self._dense_encoder = dense_encoder
        
    def _encode_documents_batch(self, documents: List[KBDocChunk]) -> List[KBEncodedDocChunk]:
        dense_values = self._dense_encoder.encode_documents([d.text for d in documents])
        return [KBEncodedDocChunk(**d.dict(), values=v) for d, v in zip(documents, dense_values)]

    def _encode_queries_batch(self, queries: List[Query]) -> List[KBQuery]:
        dense_values = self._dense_encoder.encode_queries([q.text for q in queries])
        return [KBQuery(**q.dict(), values=v) for q, v in zip(queries, dense_values)]

    async def _aencode_documents_batch(self, documents: List[KBDocChunk]) -> List[KBEncodedDocChunk]:
        raise NotImplementedError

    async def _aencode_queries_batch(self, queries: List[Query]) -> List[KBQuery]:
        raise NotImplementedError