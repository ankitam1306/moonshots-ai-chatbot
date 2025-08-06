from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import json

from bot import run_retrieval_query
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


@app.post("/ask")
async def ask(request: Request):
  response = run_retrieval_query(request.question)

  return {
		"answer": response["answer"],
		"sources": response["sources"]
	}

# uvicorn main:app --reload - to start the app
