import asyncio
import json

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

import config

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)


condense_prompt = PromptTemplate.from_template("""
Given the following conversation and a follow-up question, rephrase the follow-up question 
into a clear, standalone question that contains all necessary context from the chat history.

Do NOT drop details. If the follow-up requests "code" or "example",
make sure to explicitly reference the topic so the answer will include relevant code snippets 
in their original formatting (using triple backticks if the source includes code).

Chat History:
{chat_history}

Follow Up Question:
{question}

Standalone Question:
""")


class StreamingHandler(AsyncCallbackHandler):
    def __init__(self):
        self.queue = asyncio.Queue()
        self.answer = ""

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


def run_retrieval_query(question: str):
    if config.retriever is None:
        raise RuntimeError("Retriever not initialized. Call init_vectorstore() first.")

    stream_handler = StreamingHandler()

    llm = ChatOpenAI(model="gpt-4", temperature=0, streaming=True, callbacks=[stream_handler])

    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=config.retriever,
        memory=memory,
        return_source_documents=True,
        condense_question_prompt=condense_prompt
    )

    async def run_chain():
        # Run in background thread so we can stream while it runs
        result = await asyncio.to_thread(conv_chain.invoke, question)
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
    run_retrieval_query("How do I roll out a feature to 10% of the user")
