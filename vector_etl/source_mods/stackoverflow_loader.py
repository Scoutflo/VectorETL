import os
import requests
import pandas as pd
import logging
import time
from vector_etl.source_mods.api_base_source import ApiBaseSource

logger = logging.getLogger(__name__)

class StackOverflowSource(ApiBaseSource):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = self.config.get("STACKOVERFLOW_API_KEY")
        self.tag = self.config.get("tag", "devops")
        self.page_size = self.config.get("page_size", 10)

    def fetch_data(self):
        logger.info("Fetching latest StackOverflow questions...")
        questions = []
        base_url = "https://api.stackexchange.com/2.3/questions"
        params = {
            "order": "desc",
            "sort": "creation",
            "tagged": self.tag,
            "site": "stackoverflow",
            "pagesize": self.page_size,
        }
        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to fetch questions: {response.status_code} {response.text}")
            return pd.DataFrame()

        data = response.json()
        for item in data.get("items", []):
            question_id = item["question_id"]
            top_answer = self._get_top_answer(question_id)
            questions.append({
                "question_id": question_id,
                "title": item["title"],
                "score": item["score"],
                "link": item["link"],
                "top_answer": top_answer
            })
            time.sleep(0.2)

        df = pd.DataFrame(questions)
        return df

    def _get_top_answer(self, question_id):
        answer_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
        params = {
            "order": "desc",
            "sort": "votes",
            "site": "stackoverflow",
            "filter": "withbody"
        }
        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(answer_url, params=params)
        if response.status_code != 200:
            logger.warning(f"Failed to fetch answers for QID {question_id}: {response.status_code}")
            return ""

        answers = response.json().get("items", [])
        if answers:
            return answers[0].get("body", "")[:300]  # First 300 chars of top answer
        return ""


if __name__ == "__main__":
    import os

    logging.basicConfig(level=logging.INFO)

    config = {
        "STACKOVERFLOW_API_KEY": os.getenv("STACKOVERFLOW_API_KEY"),
        "tag": "devops",
        "page_size": 10
    }

    source = StackOverflowSource(config)
    df = source.fetch_data()
    if not df.empty:
        output_path = os.path.join(os.path.dirname(__file__), "../tempfile_downloads/stackoverflow_data.csv")
        output_path = os.path.abspath(output_path)
        source.save_to_csv(df, output_path)

