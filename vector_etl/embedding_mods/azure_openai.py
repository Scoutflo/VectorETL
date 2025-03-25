import pandas as pd
import logging
from .base import BaseEmbedding
from openai import AzureOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIEmbedding(BaseEmbedding):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            api_key=config['api_key'],
            api_version=config.get('version', '2023-05-15'),
            azure_endpoint=config['endpoint']
        )
        

    def embed(self, df, embed_column='__concat_final'):
        logger.info("Starting the Azure OpenAI embedding process...")

        text_data = df[embed_column].str.strip().tolist()

        if self.config['private_deployment'] == 'No':
            response = self.client.embeddings.create(
                input=text_data,
                model=self.config['model_name'],
                encoding_format="float"
            )
        elif self.config['private_deployment'] == 'Yes':
            response = self.client.embeddings.create(
                input=text_data,
                model=self.config['model_name']
            )
        else:
            raise ValueError("Invalid private_deployment configuration")

        embeddings = [item.embedding for item in response.data]
        df['embeddings'] = embeddings

        logger.info("Completed Azure OpenAI embedding process.")
        return df
