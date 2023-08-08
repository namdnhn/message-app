from typing import List
from pydantic import BaseModel

class Sender(BaseModel):
    id: int
    name: str
    platform: int
    
    class Config:
        orm_mode = True
        
class PlatformSender(BaseModel):
    pid: int
    senders: List[Sender]