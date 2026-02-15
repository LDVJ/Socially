from fastapi import FastAPI
from .db import Base

app = FastAPI()



@app.get("/")
def root():
    return {"message":"Welcome to Socially Platform"}


app.include_router()