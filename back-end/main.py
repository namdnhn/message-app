from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "sentry-trace", "baggage"],
)

platforms = ["Linkedin", "Facebook", "Zalo"]

@app.get("/platforms")
async def read_platforms():
    return platforms

senders = {
    "Linkedin": ["Nguyen Van A", "Nguyen Van D"],
    "Facebook": ["Nguyen Van B"],
    "Zalo": ["Nguyen Van C"],
}

@app.get("/senders")
async def get_senders():
    return senders


templates = ['template1', 'template2']

@app.get("/templates")
async def get_templates():
    return templates

