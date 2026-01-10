import asyncio

store = {}
store_lock = asyncio.Lock()


class TransactionManager:
    def __init__(self, store_ref: dict, lock: asyncio.Lock):
        self.store = store_ref
        self.lock = lock

        # Snapshot of store at transaction start
        self.working_copy = store_ref.copy()
        self.active = True

    def _ensure_active(self):
        if not self.active:
            raise RuntimeError("Transaction is no longer active")

    def set(self, key: str, value: str = "exists"):
        self._ensure_active()
        if key in self.working_copy:
            raise ValueError("Key already exists")
        self.working_copy[key] = value

    def get(self, key: str):
        self._ensure_active()
        if key not in self.working_copy:
            raise ValueError("Key does not exist")
        return self.working_copy[key]

    def delete(self, key: str):
        self._ensure_active()
        if key not in self.working_copy:
            raise ValueError("Key does not exist")
        del self.working_copy[key]

    async def commit(self):
        self._ensure_active()
        async with self.lock:
            self.store.clear()
            self.store.update(self.working_copy)
        self.active = False

    def rollback(self):
        self.active = False
