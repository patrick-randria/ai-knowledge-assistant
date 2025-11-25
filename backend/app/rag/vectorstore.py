# backend/app/rag/vectorstore.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:

    client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    def __init__(self, embedding=None):
        if not self.client.collection_exists(settings.QDRANT_COLLECTION):
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=settings.EMBED_DIM,
                    distance=Distance.COSINE
                )
            )

        # Initialisation du vectorstore Qdrant avec le client et le modèle d'embedding
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=settings.QDRANT_COLLECTION,
            embedding=embedding
        )
    
    def get_vectorstore(self):
        return self.vector_store

    def upload_documents_to_index(self, documents):

        return self.vector_store.add_documents(documents)
    
    def list_indexed_documents(self, limit=10):
        """
        List indexed documents from the Qdrant collection.
        
        Args:
            limit (int): The maximum number of documents to retrieve.

        Returns:
            List[dict]: A list of indexed documents.
        """
        try:
            response = self.client.scroll(
                collection_name=settings.QDRANT_COLLECTION,
                scroll_filter=None,  # No filter to retrieve all documents
                limit=limit,
                with_payload=True,  # Include payload (metadata) in the response
                with_vectors=False  # Exclude vectors to reduce response size
            )
            points, next_page = response  # unpack result

            document_sources = [
                point.payload['metadata'].get("source", "Unknown").split("/")[-1]
                for point in points
            ]

            return list(set(document_sources))


        except Exception as e:
            logger.error(f"Failed to list indexed documents: {e}")
            return []
        
        
