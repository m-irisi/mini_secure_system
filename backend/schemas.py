from pydantic import BaseModel

class TransactionRequest(BaseModel):
    operation: str
    key: str
