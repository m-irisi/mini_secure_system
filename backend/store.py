store = {}

class TransactionManager:
    def __init__(self, store: dict):
        # Reference to the real store
        self._store = store

        # Private copy used for staging changes
        self._working_copy = store.copy()

        # Track whether the transaction is still valid
        self._active = True

    def _ensure_active(self):
        if not self._active:
            raise RuntimeError("Transaction is no longer active")

    def set(self, key: str, value: str = "exists"):
        self._ensure_active()
        if key in self._working_copy:
            raise ValueError("Key already exists")
        self._working_copy[key] = value

    def get(self, key: str):
        self._ensure_active()
        if key not in self._working_copy:
            raise ValueError("Key does not exist")
        return self._working_copy[key]

    def delete(self, key: str):
        self._ensure_active()
        if key not in self._working_copy:
            raise ValueError("Key does not exist")
        del self._working_copy[key]

    def commit(self):
        self._ensure_active()
        self._store.clear()
        self._store.update(self._working_copy)
        self._active = False

    def rollback(self):
        self._active = False
