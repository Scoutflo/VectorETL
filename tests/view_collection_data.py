# We can use this script to view the data in a collection
import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get('CHROMA_HOST')
PORT = os.environ.get('CHROMA_PORT')

client = chromadb.HttpClient(host=HOST, port=PORT, ssl=False)
client.heartbeat()

collection_names = client.list_collections()
print(collection_names)

# We need to add collection name in the get_collection method
# results=client.get_collection(name="").peek()
# print(results)