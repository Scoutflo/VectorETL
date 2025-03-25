# we can use this script to view the data in a collection
import chromadb
client = chromadb.HttpClient(host="http://34.47.241.104:8000", port="8000", ssl=False)
client.heartbeat()

collection_names = client.list_collections()
print(collection_names)

# We need to add collection name in the get_collection method
test=client.get_collection(name="").peek()
print(test)