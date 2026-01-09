from pydantic import BaseModel, Field
from typing import Literal

class TransactionRequest(BaseModel):
    operation: Literal['set', 'get', 'delete']
    key: str = Field(pattern=r'^[A-Za-z0-9_]{1,20}$')
