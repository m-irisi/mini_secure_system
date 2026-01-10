import pytest
from backend.store import TransactionManager, store, store_lock

def setup_function():
    """
    Runs before each test.
    Ensures the store starts empty.
    """
    store.clear()

@pytest.mark.asyncio
async def test_set_and_commit():
    tm = TransactionManager(store, store_lock)

    tm.set("a")
    await tm.commit()

    assert store["a"] == "exists"

def test_get_inside_transaction():
    store["a"] = "exists"
    tm = TransactionManager(store, store_lock)

    value = tm.get("a")

    assert value == "exists"

@pytest.mark.asyncio
async def test_delete_and_commit():
    store["a"] = "exists"
    tm = TransactionManager(store, store_lock)

    tm.delete("a")
    await tm.commit()

    assert "a" not in store


def test_rollback_discards_changes():
    tm = TransactionManager(store, store_lock)

    tm.set("a")
    tm.rollback()

    assert "a" not in store


def test_atomicity_on_failure():
    tm = TransactionManager(store, store_lock)

    tm.set("a")

    with pytest.raises(ValueError):
        tm.set("a")  # duplicate key should fail

    tm.rollback()
    assert store == {}
