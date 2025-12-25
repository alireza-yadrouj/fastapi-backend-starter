from pydantic import BaseModel
from typing import Optional

class CaseCreate(BaseModel):
    title : str
    description : str


class CaseResponse(BaseModel):
    id : int
    title : str
    description : str
    owner_username: str
    
class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None