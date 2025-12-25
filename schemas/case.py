from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


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

class PaginatedCaseResponse(BaseModel):
    items: List[CaseResponse]
    page: int
    page_size: int
    total: int

class CaseSortFields(str, Enum):
    title = "title"
    description = "description"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"