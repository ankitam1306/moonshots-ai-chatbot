from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from config import init_vectorstore

from bot import run_retrieval_query_full
from model import Request

load_dotenv()

app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],  # your frontend dev server
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Example request body
class Query(BaseModel):
    question: str


@app.on_event("startup")
async def startup_event():
   init_vectorstore()


@app.post("/ask")
async def ask(request: Request):
  response = run_retrieval_query_full(request.question)
  return {
		  "answer": response["answer"],
		  "sources": response["sources"]
	  }
  # return StreamingResponse(
  #   run_retrieval_query(request.question),
  #   media_type="text/plain"
  # )

# uvicorn main:app --reload - to start the app
