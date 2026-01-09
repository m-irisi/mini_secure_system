from fastapi import FastAPI, HTTPException
from backend.schemas import TransactionRequest
from backend.store import store

app = FastAPI()

@app.get("/") 
def health_check():
    return {"status": "ok"}

@app.post("/transaction")
def transaction(request: TransactionRequest):
    if request.operation == 'set':
        if request.key in store:
            raise HTTPException(status_code=400, detail="Key already exists.")
        store[request.key] = "exists"
        return {
            "operation": request.operation,
            "key": request.key,
            "value": store[request.key]
        }
    elif request.operation == 'get':
        if request.key not in store:
            raise HTTPException(status_code=400, detail="Key does not exist.")
        return {
            "operation": request.operation,
            "key": request.key,
            "value": store[request.key]
        }
    elif request.operation == 'delete':
        if request.key not in store:
            raise HTTPException(status_code=400, detail="Key does not exist.")
        del store[request.key]
        return {
            "operation": request.operation,
            "key": request.key,
            "value": None  # key no longer exists
        }
    return {
        "operation": request.operation,
        "key": request.key
    }