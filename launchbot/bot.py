from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks.base import AsyncCallbackHandler
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate

import asyncio
import json

from config import PINECONE_INDEX_NAME
import config

CUSTOM_RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a LaunchDarkly documentation assistant. Use the following retrieved documentation context to answer the user’s question.

If the context is insufficient, use best practices and general knowledge of LaunchDarkly, but clearly indicate which parts were inferred.

Format your response using markdown with **bolded section headers**, bullet points, and code snippets when appropriate.

---

Context:
{context}

---

Question:
{question}

Answer:
"""
)


class StreamingHandler(AsyncCallbackHandler):
	def __init__(self):
		self.queue = asyncio.Queue()
		self.answer = ''
		
	async def on_llm_new_token(self, token: str, **kwargs):
		self.answer += token
		await self.queue.put(token)
	
	async def on_chat_model_start(self, *args, **kwargs):
		pass
	
	async def on_llm_end(self, *args, **kwargs):
		pass
	
	async def on_llm_error(self, *args, **kwargs):
		pass

	async def token_generator(self):
		while True:
			token = await self.queue.get()
			if token is None:
				break
			yield token


def run_retrieval_query_full(question: str):
	embedding_model = OpenAIEmbeddings()
	vectorstore = PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embedding_model)
	retriever = vectorstore.as_retriever(search_type="similarity", k=8)
	llm = ChatOpenAI(model="gpt-4", temperature=0)
	qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": CUSTOM_RAG_PROMPT})
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


def run_retrieval_query(question: str):
  
	if config.retriever is None:
		raise RuntimeError("Retriever not initialized. Call init_vectorestore() first.")

	stream_handler = StreamingHandler()
	llm = ChatOpenAI(model = "gpt-4", temperature = 0, streaming=True, callbacks=[stream_handler])
 
	qa_chain = RetrievalQA.from_chain_type(llm = llm, retriever = config.retriever, return_source_documents=True, chain_type_kwargs={"prompt": CUSTOM_RAG_PROMPT})
	
	async def run_chain():
		result = await asyncio.to_thread(qa_chain.invoke, question)
  
		sources = {doc.metadata.get("source", "unknown") for doc in result["source_documents"]}
  
		final_payload = json.dumps({"type": "sources", "sources": list(sources)})
		await stream_handler.queue.put(f"\n\n{final_payload}")
		await stream_handler.queue.put(None)
		
	asyncio.create_task(run_chain())
 
	return stream_handler.token_generator()


if __name__ == "__main__":
	# run_retrieval_query("How do you install ldcli on macOS using Homebrew")
	# run_retrieval_query("Which environment variable is used to authenticate ldcli with LaunchDarkly?")
	# run_retrieval_query("How do you verify the version of ldcli installed on your system?")
	# run_retrieval_query("How to create access token")
	# run_retrieval_query("How to check usage information")
	run_retrieval_query_full("what is a guarded rollout and how can I use that?")

