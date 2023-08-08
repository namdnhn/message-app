from fastapi_camelcase import CamelModel

class Platform(CamelModel):
    id: int
    name: str
    
    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        return isinstance(other, Platform) and self.id == other.id and self.name == other.name
    
    class Config:
        orm_mode = True