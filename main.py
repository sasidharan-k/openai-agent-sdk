import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print("API Key", os.getenv("OPENAI_API_KEY"))
test_agent = Agent(name="Assistant", instructions="You are a helpful assistant")

app = FastAPI()
# Request Model
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Heroku!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.post("/chat")
async def say_chat(request: QuestionRequest):
    try:
        result = await Runner.run(test_agent, request.question)
        return result.final_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
