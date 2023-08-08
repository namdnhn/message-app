from fastapi_camelcase import CamelModel

class Platform(CamelModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True