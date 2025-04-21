import chromadb
from chromadb.config import Settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chromadb():
    client = chromadb.PersistentClient(path="./chroma_data")
    
    # Fetch the collection
    collection_name = "stackoverflow_qa"
    logger.info(f"Fetching collection: {collection_name}")
    collection = client.get_collection(name=collection_name)

    # Query all entries
    results = collection.get(include=['documents', 'embeddings', 'metadatas'])

    logger.info(f"Total entries retrieved: {len(results['ids'])}")

    for i in range(len(results['ids'])):
        print(f"\n--- Entry {i+1} ---")
        print(f"ID: {results['ids'][i]}")
        print(f"Metadata: {results['metadatas'][i]}")
        print(f"Document: {results['documents'][i]}")
        
        # Check if embedding exists and preview first few dimensions
        embedding = results['embeddings'][i]
        if embedding is not None:
            print(f"Embedding (first 10 values): {embedding[:10]}")
        else:
            print("No embedding found.")

if __name__ == "__main__":
    test_chromadb()

