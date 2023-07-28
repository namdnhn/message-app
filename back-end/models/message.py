import uvicorn
from fastapi import FastAPI
from fastapi_camelcase import CamelModel

class Message(CamelModel):
    id: int
    platform: int
    receiver: int
    url_receiver: str
    message_content: str
    already_connected: bool
    change_position: bool
    follow_candidate: bool
    
    class Config:
        orm_mode = True