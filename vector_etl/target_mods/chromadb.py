import logging
import pandas as pd
import chromadb
from chromadb.config import Settings
from .base import BaseTarget

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaDBTarget(BaseTarget):
    def __init__(self, config):
        self.config = config
        self.client = None
        self.collection = None

   
    def connect(self):
        logger = logging.getLogger(__name__)
        logger.info("Connecting to ChromaDB...")

        if 'persist_directory' in self.config:
            logger.info("Using PersistentClient (embedded ChromaDB)...")
            self.client = chromadb.PersistentClient(path=self.config['persist_directory'])
        else:
            logger.info(f"Using HttpClient (ChromaDB server) at {self.config['host']}:{self.config['port']}...")
            self.client = chromadb.HttpClient(
                host=self.config['host'],
                port=self.config['port'],
                ssl=self.config.get('ssl', False)
            )
            self.client.heartbeat()

        logger.info("Connected to ChromaDB successfully.")


    def create_index_if_not_exists(self, dimension):
        if self.client is None:
            self.connect()

        collection_name = self.config["collection_name"]
        
        collection_names = self.client.list_collections()
        
        if collection_name not in collection_names:
            logger.info(f"Creating ChromaDB collection: {collection_name}")
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"dimension": dimension}
            )
        else:
            self.collection = self.client.get_collection(name=collection_name)

    def write_data(self, df, columns, domain=None):
        logger.info("Writing embeddings to ChromaDB...")
        if self.collection is None:
            self.create_index_if_not_exists(len(df['embeddings'].iat[0]))

        upload_data = []
        ids = []
        embeddings = []
        metadatas = []
        
        for _, row in df.iterrows():
            if len(columns) > 0:
                columns.append("__concat_final")
                metadata_data = {col: str(row[col]) for col in columns}
                
                data = {
                    "id": str(row["df_uuid"]),
                    "embedding": row["embeddings"],
                    "metadata": metadata_data
                }
                columns.remove("__concat_final")
            elif len(columns) == 0:
                data = {
                    "id": str(row["df_uuid"]),
                    "embedding": row["embeddings"],
                    "metadata": {
                        col: str(row[col]) if isinstance(row[col], list) else str(row[col])
                        for col in df.columns if col not in ["df_uuid", "embeddings"] and pd.notna(row[col])
                    }
                }
            if domain:
                data["metadata"]["domain"] = domain
            
            ids.append(data["id"])
            embeddings.append(data["embedding"])
            metadatas.append(data["metadata"])
            
        # ChromaDB requires documents, but we're not using them for embedding storage
        documents = [""] * len(ids)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        
        logger.info("Completed writing embeddings to ChromaDB.")
