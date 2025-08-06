import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://launchdarkly.com/docs/"
DOMAIN = "launchdarkly.com"

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
