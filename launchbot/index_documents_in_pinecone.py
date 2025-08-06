from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from crawler import get_all_documents

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def chunk_documents(documents):
	splitter = RecursiveCharacterTextSplitter(chunk_size=1300, chunk_overlap=200)
	return splitter.split_documents(documents)


def index_documents():
	documents = get_all_documents(start_url="https://launchdarkly.com/docs/", max_workers=10)
	print("Finished crawling documents. Total documents fetched: ", len(documents))
	chunks = chunk_documents(documents)
	print("Chunks created: ", len(chunks))
	if not chunks:
			print("No chunks to index.")
			return
	embedding_model = OpenAIEmbeddings()
	vectorstore = PineconeVectorStore.from_documents(documents=chunks,
																										embedding=embedding_model,
																										index_name=PINECONE_INDEX_NAME,
																										pinecone_api_key=PINECONE_API_KEY)
	print(f"Done uploading to Pinecone")


if __name__ == "__main__":
    index_documents()
