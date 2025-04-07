import os
from .stackoverflow_loader import StackOverflowSource

if __name__ == "__main__":
    config = {
        "STACKOVERFLOW_API_KEY": os.getenv("STACKOVERFLOW_API_KEY"),
        "tag": "devops",
        "page_size": 5
    }

    source = StackOverflowSource(config)
    df = source.fetch_data()
    df.to_csv("tempfiles_downloads/stackoverflow_test.csv", index=False)
    print("StackOverflow test data saved!")

