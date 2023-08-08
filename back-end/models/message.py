from pydantic import Field, BaseModel

class SendMessageRequest(BaseModel):
    platform: int = Field(..., gt=0)
    receiver: int = Field(..., gt=0)
    url_receiver: str = Field(..., min_length=1, alias="urlReceiver")
    message_content: str = Field(..., min_length=1, alias="messageContent")
    already_connected: bool = Field(..., description="Must be True or False", alias="alreadyConnected")
    change_position: bool = Field(..., description="Must be True or False", alias="changePosition")
    follow_candidate: bool = Field(..., description="Must be True or False", alias="followCandidate")

        
class GetMessageRequest(BaseModel):
    id: int
    platform: int
    receiver: int
    url_receiver: str = Field(alias="urlReceiver")
    message_content: str = Field(alias="messageContent")
    already_connected: bool = Field(alias="alreadyConnected")
    change_position: bool = Field(alias="changePosition")
    follow_candidate: bool = Field(alias="followCandidate")