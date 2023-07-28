import uvicorn
from fastapi import FastAPI
from fastapi_camelcase import CamelModel

class Sender(CamelModel):
    id: int
    name: str
    platform: int
    
    class Config:
        orm_mode = True