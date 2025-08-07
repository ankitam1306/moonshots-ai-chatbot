import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

BASE_URL = "https://launchdarkly.com/docs/"
DOMAIN = "launchdarkly.com"

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

retriever = None

def init_vectorstore():
  """Initialize Pinecone retriever once. """
  global retriever
  embedding_model = OpenAIEmbeddings()
  vectorstore = PineconeVectorStore.from_existing_index(index_name = PINECONE_INDEX_NAME, embedding = embedding_model)
  retriever = vectorstore.as_retriever(search_type = "similarity", k = 8)
  print(f"Vectore store initialized once and retriever cached.")