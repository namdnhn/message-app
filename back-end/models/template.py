from pydantic import Field, BaseModel
class SendTemplateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    template: str = Field(..., min_length=1)
    
    class Config:
        orm_mode = True
        
class GetTemplateRequest(BaseModel):
    id: int
    name: str
    template: str
    
    class Config:
        orm_mode = True