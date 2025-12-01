
import sys
from pathlib import Path
import time
import json

# Add src to path
project_root = Path.cwd()
sys.path.insert(0, str(project_root / "src"))

from gfs_client import GFSClient
from data_loader import scan_documents, check_gfs_compatibility
from utils import load_api_key

def main():
    print("Starting verification...")
    
    # Load API key
    try:
        api_key = load_api_key("GOOGLE_API_KEY", str(project_root / ".env"))
    except Exception as e:
        print(f"Error loading API key: {e}")
        return

    # Initialize client
    print("Initializing GFSClient...")
    gfs = GFSClient(api_key=api_key, model_id="gemini-2.5-flash")
    
    # List stores
    print("Listing stores...")
    stores = gfs.list_stores()
    print(f"Found {len(stores)} stores.")
    
    store_display_name = "RAG Verification Store"
    store = None
    
    # Check if verification store exists
    for s in stores:
        if s.display_name == store_display_name:
            store = s
            print(f"Found existing verification store: {store.name}")
            break
            
    if not store:
        print("Creating new store...")
        store = gfs.create_file_search_store(display_name=store_display_name)
        print(f"Created store: {store.name}")
        
    # Scan documents
    data_dir = project_root / "data" / "raw"
    print(f"Scanning documents in {data_dir}...")
    df = scan_documents(data_dir)
    df_compat = check_gfs_compatibility(df)
    compatible_files = df_compat.filter(df_compat["gfs_compatible"])
    
    print(f"Found {len(compatible_files)} compatible files.")
    
    # Upload one file for testing
    if len(compatible_files) > 0:
        row = compatible_files.row(0, named=True)
        file_path = Path(row["file_path"])
        print(f"Uploading {file_path.name}...")
        
        try:
            gfs.upload_to_store(store.name, file_path, wait_for_completion=True)
            print("Upload successful.")
        except Exception as e:
            print(f"Upload failed: {e}")
            # Continue to query test if possible (maybe file was already there)
            
    # Test Query
    query = "What is this document about?"
    print(f"Testing query: '{query}'")
    try:
        response = gfs.query_with_file_search(
            query=query,
            store_names=[store.name]
        )
        print("Response received:")
        print(response.text[:200] + "...")
        
        citations = gfs.extract_citations(response)
        if citations:
            print("Citations found.")
        else:
            print("No citations found.")
            
    except Exception as e:
        print(f"Query failed: {e}")

    # Cleanup (optional, maybe keep it for inspection)
    # print("Deleting store...")
    # gfs.delete_store(store.name)

if __name__ == "__main__":
    main()
