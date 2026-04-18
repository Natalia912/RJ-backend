from pydantic import BaseModel

class CreateResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str