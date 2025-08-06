from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from config import PINECONE_INDEX_NAME

def run_retrieval_query(question: str):
	embedding_model = OpenAIEmbeddings()
	vectorstore = PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embedding_model)
	retriever = vectorstore.as_retriever(search_type="similarity", k=8)
	llm = ChatOpenAI(model="gpt-4", temperature=0)
	qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
	result = qa_chain.invoke(question)
	print(f'Source is: {result["source_documents"]}')

	print("💬 Answer:\n", result["result"])
	unique_sources = set()
	for doc in result["source_documents"]:
		src = doc.metadata.get("source", "unknown")
		unique_sources.add(src)

	print("\n📚 Sources:")
	for src in unique_sources:
		print("•", src)

	# unique_sources = list({doc.metadata.get("source", "unknown") for doc in result["source_documents"]})

	return {
		"answer": result["result"],
		"sources": unique_sources
	}


if __name__ == "__main__":
	# run_retrieval_query("How do you install ldcli on macOS using Homebrew")
	# run_retrieval_query("Which environment variable is used to authenticate ldcli with LaunchDarkly?")
	# run_retrieval_query("How do you verify the version of ldcli installed on your system?")
	# run_retrieval_query("How to create access token")
	# run_retrieval_query("How to check usage information")
	run_retrieval_query("what is a guarded rollout and how can I use that?")

