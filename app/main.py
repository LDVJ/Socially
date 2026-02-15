from fastapi import FastAPI
from .db import Base,engine
from . import models
from .routes import users

models.Base.metadata.create_all(bind = engine)

app = FastAPI()



@app.get("/")
def root():
    return {"message":"Welcome to Socially Platform"}


app.include_router(users.router)