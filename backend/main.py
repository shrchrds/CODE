# backend/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Shri Hari!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}