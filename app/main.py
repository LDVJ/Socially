from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base,engine
from . import models
from .routes import users, authentication,posts
from .services import post_like

# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials =True,
    allow_headers = ["*"],
    allow_methods= ["*"]
    )

@app.get("/")
def root():
    return {"message":"Welcome to Socially Platform"}

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)

app.include_router(post_like.router)