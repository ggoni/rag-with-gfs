"""Google Generative File Search (GFS) client wrapper"""

import time
from pathlib import Path
from typing import Optional, List

from google import genai
from google.genai import types


class GFSClient:
    """Wrapper for Google Generative File Search API"""

    def __init__(self, api_key: str, model_id: str = "gemini-2.0-flash-exp"):
        """
        Initialize GFS client.

        Args:
            api_key: Google API key
            model_id: Gemini model to use
        """
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id

    def create_file_search_store(self, display_name: str) -> types.FileSearchStore:
        """
        Create a new file search store.

        Args:
            display_name: Human-readable name for the store

        Returns:
            FileSearchStore object
        """
        store = self.client.file_search_stores.create(
            config=types.CreateFileSearchStoreConfig(display_name=display_name)
        )
        return store

    def upload_file(
        self,
        file_path: Path,
        display_name: Optional[str] = None,
        mime_type: Optional[str] = None
    ) -> types.File:
        """
        Upload a file to GFS.

        Args:
            file_path: Path to file
            display_name: Optional display name
            mime_type: Optional MIME type

        Returns:
            File object
        """
        config = types.UploadFileConfig(
            display_name=display_name or file_path.name,
            mime_type=mime_type
        )

        file_obj = self.client.files.upload(
            file=str(file_path),
            config=config
        )

        # Wait for processing
        while file_obj.state.name == "PROCESSING":
            time.sleep(2)
            file_obj = self.client.files.get(name=file_obj.name)

        return file_obj

    def upload_to_store(
        self,
        store_name: str,
        file_path: Path,
        wait_for_completion: bool = True
    ) -> types.Operation:
        """
        Upload file to a file search store.

        Args:
            store_name: Name of the store
            file_path: Path to file
            wait_for_completion: Whether to wait for upload to complete

        Returns:
            Operation object
        """
        # First upload the file
        file_obj = self.upload_file(file_path)

        # Then add to store
        operation = self.client.file_search_stores.upload_to_file_search_store(
            name=store_name,
            file=file_obj
        )

        if wait_for_completion:
            while not operation.done:
                time.sleep(5)
                operation = self.client.operations.get(operation)

        return operation

    def query_with_file_search(
        self,
        query: str,
        store_names: List[str],
        temperature: float = 0.0,
        top_k: Optional[int] = None,
        metadata_filter: Optional[str] = None
    ) -> types.GenerateContentResponse:
        """
        Query using file search tool.

        Args:
            query: User query
            store_names: List of file search store names to query
            temperature: Generation temperature (0.0 for factual)
            top_k: Maximum number of results to return
            metadata_filter: Filter expression for metadata

        Returns:
            GenerateContentResponse with answer and grounding
        """
        # Use the first store name (API expects single store)
        store_name = store_names[0] if store_names else None

        if not store_name:
            raise ValueError("At least one store name is required")

        # Create tool with FileSearchTool using file_search_store parameter
        tool = types.Tool(
            file_search_tool=types.FileSearchTool(
                file_search_store=store_name
            )
        )

        # Generate response
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=query,
            config=types.GenerateContentConfig(
                tools=[tool],
                temperature=temperature
            )
        )

        return response

    def list_stores(self) -> List[types.FileSearchStore]:
        """
        List all file search stores.

        Returns:
            List of FileSearchStore objects
        """
        stores = []
        response = self.client.file_search_stores.list()

        for store in response:
            stores.append(store)

        return stores

    def get_store_info(self, store_name: str) -> types.FileSearchStore:
        """
        Get information about a file search store.

        Args:
            store_name: Name of the store

        Returns:
            FileSearchStore object with metadata
        """
        return self.client.file_search_stores.get(name=store_name)

    def delete_store(self, store_name: str) -> None:
        """
        Delete a file search store.

        Args:
            store_name: Name of the store to delete
        """
        self.client.file_search_stores.delete(name=store_name)

    def extract_citations(
        self,
        response: types.GenerateContentResponse
    ) -> Optional[dict]:
        """
        Extract grounding/citation information from response.

        Args:
            response: GenerateContentResponse

        Returns:
            Dictionary with citation info or None
        """
        if not response.candidates:
            return None

        candidate = response.candidates[0]
        grounding = candidate.grounding_metadata

        if not grounding:
            return None

        return {
            "search_entry_point": grounding.search_entry_point,
            "grounding_chunks": grounding.grounding_chunks if hasattr(grounding, "grounding_chunks") else None,
            "grounding_supports": grounding.grounding_supports if hasattr(grounding, "grounding_supports") else None,
        }
