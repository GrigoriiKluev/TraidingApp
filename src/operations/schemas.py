from datetime import datetime
from typing import Optional, List

from operations.models import operation
from pydantic import BaseModel


class OperationRead(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str|None # Принимает либо строку либо Null
    date: datetime
    type: str

    class Config:
        orm_mode = True

class OperationsWithStatus(BaseModel):
    status: str
    data: List[OperationRead]
    details : str|None

    class Config:
        orm_mode = True








class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str | None  # Принимает либо строку либо Null
    date: datetime
    type: str