"""Custom RAG implementation using ChromaDB and sentence-transformers"""

import time
from pathlib import Path
from typing import List, Optional, Dict
import hashlib

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types


class CustomRAG:
    """Custom RAG implementation for baseline comparison"""

    def __init__(
        self,
        api_key: str,
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "gemini-2.0-flash-exp",
        persist_directory: Optional[Path] = None
    ):
        """
        Initialize custom RAG system.

        Args:
            api_key: Google API key for LLM
            embedding_model: HuggingFace embedding model
            llm_model: Gemini model for generation
            persist_directory: Directory to persist ChromaDB
        """
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize vector database
        client_settings = Settings(
            persist_directory=str(persist_directory) if persist_directory else None,
            anonymized_telemetry=False
        )
        self.chroma_client = chromadb.Client(client_settings)

        # Initialize LLM client
        self.llm_client = genai.Client(api_key=api_key)
        self.llm_model = llm_model

        self.collection = None

    def create_collection(self, collection_name: str, recreate: bool = False) -> None:
        """
        Create or get ChromaDB collection.

        Args:
            collection_name: Name of the collection
            recreate: Whether to delete and recreate existing collection
        """
        if recreate:
            try:
                self.chroma_client.delete_collection(name=collection_name)
            except Exception:
                pass

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 512,
        overlap: int = 50
    ) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            chunk_size: Approximate characters per chunk
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []

        # Approximate words per chunk
        words_per_chunk = chunk_size // 5  # Rough estimate

        for i in range(0, len(words), words_per_chunk - overlap // 5):
            chunk = " ".join(words[i:i + words_per_chunk])
            if chunk:
                chunks.append(chunk)

        return chunks

    def index_document(
        self,
        file_path: Path,
        chunk_size: int = 512,
        overlap: int = 50,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Index a document into the vector database.

        Args:
            file_path: Path to document
            chunk_size: Characters per chunk
            overlap: Overlap between chunks
            metadata: Additional metadata

        Returns:
            Number of chunks indexed
        """
        if self.collection is None:
            raise ValueError("Collection not created. Call create_collection() first.")

        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Chunk text
        chunks = self.chunk_text(text, chunk_size, overlap)

        # Generate embeddings
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)

        # Prepare metadata
        file_metadata = metadata or {}
        file_metadata["source_file"] = file_path.name
        file_metadata["file_path"] = str(file_path)

        # Create unique IDs for chunks
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:8]

        # Add to collection
        self.collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=[{**file_metadata, "chunk_id": i} for i in range(len(chunks))],
            ids=[f"{file_hash}_{i}" for i in range(len(chunks))]
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: User query
            top_k: Number of chunks to retrieve

        Returns:
            Dictionary with chunks, distances, and metadata
        """
        if self.collection is None:
            raise ValueError("Collection not created.")

        # Encode query
        query_embedding = self.embedding_model.encode([query], show_progress_bar=False)

        # Query collection
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k
        )

        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
        }

    def generate_answer(
        self,
        query: str,
        context: List[str],
        temperature: float = 0.0
    ) -> types.GenerateContentResponse:
        """
        Generate answer using retrieved context.

        Args:
            query: User query
            context: Retrieved text chunks
            temperature: Generation temperature

        Returns:
            GenerateContentResponse
        """
        # Build prompt with context
        context_str = "\n\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(context)])

        prompt = f"""You are a helpful assistant. Answer the question based on the provided context.

Context:
{context_str}

Question: {query}

Answer:"""

        response = self.llm_client.models.generate_content(
            model=self.llm_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temperature)
        )

        return response

    def query(
        self,
        query: str,
        top_k: int = 5,
        temperature: float = 0.0
    ) -> Dict:
        """
        End-to-end RAG query.

        Args:
            query: User query
            top_k: Number of chunks to retrieve
            temperature: Generation temperature

        Returns:
            Dictionary with answer, context, and metrics
        """
        start_time = time.time()

        # Retrieve
        retrieval_start = time.time()
        retrieval_results = self.retrieve(query, top_k)
        retrieval_time = time.time() - retrieval_start

        # Generate
        generation_start = time.time()
        response = self.generate_answer(
            query=query,
            context=retrieval_results["documents"],
            temperature=temperature
        )
        generation_time = time.time() - generation_start

        total_time = time.time() - start_time

        return {
            "answer": response.text,
            "context": retrieval_results["documents"],
            "distances": retrieval_results["distances"],
            "metadatas": retrieval_results["metadatas"],
            "metrics": {
                "retrieval_time": retrieval_time,
                "generation_time": generation_time,
                "total_time": total_time,
                "num_chunks_retrieved": len(retrieval_results["documents"])
            }
        }

    def get_stats(self) -> Dict:
        """
        Get collection statistics.

        Returns:
            Dictionary with collection stats
        """
        if self.collection is None:
            return {}

        count = self.collection.count()
        return {
            "collection_name": self.collection.name,
            "total_chunks": count,
            "embedding_dimension": self.embedding_dim
        }
