from pydantic import BaseModel

class CaseCreate(BaseModel):
    title : str
    description : str


class CaseResponse(BaseModel):
    id : int
    title : str
    description : str
    