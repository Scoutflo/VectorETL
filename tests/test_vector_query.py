import os
from dotenv import load_dotenv
import chromadb
from openai import AzureOpenAI

load_dotenv()

def get_azure_embedding_client():
    return AzureOpenAI(
        azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
        api_key=os.environ.get('AZURE_OPENAI_KEY'),
        api_version="2023-05-15"
    )

def generate_embedding(client, text):
    response = client.embeddings.create(
        input=text, 
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

def connect_to_chroma():
    HOST = os.environ.get('CHROMA_HOST')
    PORT = os.environ.get('CHROMA_PORT')
    
    try:
        client = chromadb.HttpClient(host=HOST, port=PORT, ssl=False)
        client.heartbeat()
        return client
    except Exception as e:
        print(f"Error connecting to Chroma DB: {e}")
        return None

def query_collection(client, azure_client, collection_name, query_text, n_results=5):
    try:
        # Generate embedding for the query
        query_embedding = generate_embedding(azure_client, query_text)
        
        # Get the collection and query
        collection = client.get_collection(name=collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Error querying collection {collection_name}: {e}")
        return None

def main():
    chroma_client = connect_to_chroma()
    if not chroma_client:
        return
    
    azure_client = get_azure_embedding_client()
    
    collection_name = "collection name"
    query_text = "test query"
    
    results = query_collection(chroma_client, azure_client, collection_name, query_text)
    
    if results:
        print(results)

if __name__ == "__main__":
    main()