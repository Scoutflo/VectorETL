from vector_etl.target_mods.chromadb import ChromaDBTarget
import pandas as pd
import numpy as np

def sample_df():
    return pd.DataFrame({
        'df_uuid': ['uuid1', 'uuid2'],
        'embeddings': [np.random.rand(1536), np.random.rand(1536)],
        'text': ['This is a test sentence.', 'Another test sentence.'],
        'metadata': [{'version': 'value1'}, {'module': 'value2'}]
    })

config = {
        'host': 'http://34.47.241.104:8000',
        # 'chromadb_api_key': 'test_api_key',
        'port': 8000,
        'collection_name': 'scoutflo-test-v2'
    }

def run():
    
    target = ChromaDBTarget(config)
    target.connect()
    target.write_data(sample_df(), columns=[], domain='test_domain')
        
        
if __name__ == "__main__":
    run()