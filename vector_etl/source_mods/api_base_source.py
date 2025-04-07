from abc import ABC, abstractmethod
import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class ApiBaseSource(ABC):
    def __init__(self, config):
        self.config = config
        self.output_dir = os.path.join(os.getcwd(), "vector_etl", "tempfile_downloads")
        os.makedirs(self.output_dir, exist_ok=True)

    @abstractmethod
    def fetch_data(self):
        """Fetch data from the API and return as a DataFrame."""
        pass

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved data to {output_path}")
        return output_path

