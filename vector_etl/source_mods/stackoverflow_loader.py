import os
import requests
import pandas as pd
import logging
import time
import html
from vector_etl.source_mods.api_base_source import ApiBaseSource
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)

class StackOverflowSource(ApiBaseSource):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = self.config.get("STACKOVERFLOW_API_KEY")
        self.tag = self.config.get("tag", "python")
        self.page_size = self.config.get("page_size", 10)

    def clean_html(self, raw_html): 
        return BeautifulSoup(raw_html, "html.parser").get_text()
     
   
    def fetch_data(self):
        logger.info("Fetching high-quality StackOverflow Q&A with accepted answers...")
        questions_data = []
        base_url = "https://api.stackexchange.com/2.3/search/advanced"
        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": self.tag,
            "site": "stackoverflow",
            "pagesize": self.page_size,
            "accepted": True,
            "answers": 1
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
            title = item["title"]
            link = item["link"]
            score = item["score"]
            accepted_answer_id = item.get("accepted_answer_id")

            # Fetch question body
            q_url = f"https://api.stackexchange.com/2.3/questions/{question_id}"
            q_params = {"site": "stackoverflow", "filter": "withbody"}
            if self.api_key:
                q_params["key"] = self.api_key

            q_res = requests.get(q_url, params=q_params)
            if q_res.status_code != 200:
                logger.warning(f"Failed to fetch body for QID {question_id}")
                continue
            question_body = html.unescape(q_res.json()["items"][0].get("body", ""))

            # Fetch accepted answer body
            a_url = f"https://api.stackexchange.com/2.3/answers/{accepted_answer_id}"
            a_params = {"site": "stackoverflow", "filter": "withbody"}
            if self.api_key:
                a_params["key"] = self.api_key

            a_res = requests.get(a_url, params=a_params)
            if a_res.status_code != 200:
                logger.warning(f"Failed to fetch accepted answer for QID {question_id}")
                continue
            answer_body = html.unescape(a_res.json()["items"][0].get("body", ""))

            if question_body.strip() and answer_body.strip():
                clean_q = self.clean_html(question_body)[:2000]
                clean_a = self.clean_html(answer_body)[:2000]
                combined_text = f"Title: {title} ~ Question: {clean_q} ~ Answer: {clean_a}"

                questions_data.append({
                    "question_id": question_id,
                    "title": title,
                    "question_body": clean_q,
                    "accepted_answer": clean_a,
                    "combined_text": combined_text,
                    "score": score,
                    "link": link
                })

            time.sleep(0.3)

        df = pd.DataFrame(questions_data)

        if not df.empty:
            output_dir = os.path.join(os.path.dirname(__file__), "../tempfile_downloads")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.abspath(os.path.join(output_dir, "stackoverflow_data.csv"))
            df.to_csv(output_path, index=False)
            logger.info(f" Q&A data saved to {output_path}")
        else:
            logger.warning("No suitable questions found.")

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
            raw_body = answers[0].get("body", "")
            cleaned_body = html.unescape(raw_body)
            return cleaned_body[:1000]  # limit to 1000 chars
        else:
            logger.info(f"No answers found for question ID {question_id}")
        return ""




if __name__ == "__main__":
    import os
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    config = {
        "STACKOVERFLOW_API_KEY": os.getenv("STACKOVERFLOW_API_KEY"),
        "tag": "python",
        "page_size": 10
    }

    source = StackOverflowSource(config)
    df = source.fetch_data()  

    if not df.empty:
        source.save_to_csv(df, "stackoverflow_data.csv")
    else:
        logger.warning("DataFrame is empty. CSV not saved.")

