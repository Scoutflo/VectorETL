from setuptools import setup, find_packages
# from vector_etl import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vector-etl",
    version="0.1.7",
    author="Jide Ogunjobi",
    author_email="jide@contextdata.ai",
    description="Lightweight ETL pipeline for processing data into vector databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ContextData/vector_etl",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "boto3",
        "botocore",
        "cohere",
        "cffi",
        "openai",
        "psycopg2-binary",
        "pinecone-client",
        "requests",
        "tiktoken",
        "python-dotenv",
        "pydantic",
        "mysql-connector-python",
        "pymysql",
        "pandas",
        "qdrant-client",
        "singlestoredb",
        "weaviate-client",
        "azure-storage-blob",
        "google-cloud-storage",
        "snowflake-connector-python",
        "stripe",
        "vecs",
        "simple-salesforce",
        "google-generativeai",
        "anthropic",
        "pympler",
        "unstructured[all-docs]",
        "dropbox",
        "zenpy",
        "lancedb",
        "pyyaml",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "unstructured-client",
        "box-sdk-gen",
        "pymongo",
        "neo4j",
        "python-magic",
        "pytest",
        "nltk",
        "pymilvus",
    ],
    entry_points={
        "console_scripts": [
            "vector-etl=vector_etl.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "vector_etl": ["config/examples/*.yaml"],
    },
)