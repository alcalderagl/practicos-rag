from src.chunking.mylib.chunking_logic import greeting
import uvicorn
from fastapi import FastAPI
from src.chunking.mylib.cleaning_text_logic import clean_doc
from src.chunking.mylib.chunking_logic import chuck_doc
from src.chunking.mylib.Document import Document

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/greeting/{person}")
async def greetingTo(person: str):
    return {"message": f"hello there, {person} !"}

@app.post("/chuncking/docs/cleaning_text")
async def clean_text(doc:Document):
    resp = clean_doc(doc)
    return {"message": resp }

@app.post("/chuncking/docs")
async def chunking(doc: Document):
    resp = chuck_doc(doc)
    return resp
    

