import uvicorn
from fastapi import FastAPI
from fastapi_camelcase import CamelModel

class Template(CamelModel):
    id: int
    name: str
    template: str
    
    class Config:
        orm_mode = True