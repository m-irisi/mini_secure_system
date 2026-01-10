import asyncio
from backend.store import store, store_lock, TransactionManager

async def run_transaction(key):
    tm = TransactionManager(store, store_lock)
    tm.set(key)
    await tm.commit()

async def main():
    store.clear()

    await asyncio.gather(
        run_transaction("x"),
        run_transaction("y"),
    )

    print(store)

def test_concurrent_transactions():
    asyncio.run(main())
