from fastapi import FastAPI, HTTPException, Body
from typing import List
from backend.schemas import TransactionRequest
from backend.store import TransactionManager, store, store_lock

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

@app.post("/batch")
async def batch(operations: List[TransactionRequest] = Body(...)):
    tm = TransactionManager(store, store_lock)

    try:
        results = []

        for op in operations:
            if op.operation == "set":
                tm.set(op.key)
                results.append({
                    "operation": "set",
                    "key": op.key,
                    "value": tm.get(op.key)
                })

            elif op.operation == "get":
                value = tm.get(op.key)
                results.append({
                    "operation": "get",
                    "key": op.key,
                    "value": value
                })

            elif op.operation == "delete":
                tm.delete(op.key)
                results.append({
                    "operation": "delete",
                    "key": op.key,
                    "value": None
                })

        await tm.commit()
        return results

    except ValueError as e:
        tm.rollback()
        raise HTTPException(status_code=400, detail=str(e))
