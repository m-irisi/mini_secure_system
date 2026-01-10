import pytest
from backend.store import TransactionManager, store

def setup_function():
    """
    Runs before each test.
    Ensures the store starts empty.
    """
    store.clear()


def test_set_and_commit():
    tm = TransactionManager(store)

    tm.set("a")
    tm.commit()

    assert store["a"] == "exists"


def test_get_inside_transaction():
    store["a"] = "exists"
    tm = TransactionManager(store)

    value = tm.get("a")

    assert value == "exists"


def test_delete_and_commit():
    store["a"] = "exists"
    tm = TransactionManager(store)

    tm.delete("a")
    tm.commit()

    assert "a" not in store


def test_rollback_discards_changes():
    tm = TransactionManager(store)

    tm.set("a")
    tm.rollback()

    assert "a" not in store


def test_atomicity_on_failure():
    tm = TransactionManager(store)

    tm.set("a")

    with pytest.raises(ValueError):
        tm.set("a")  # duplicate key should fail

    tm.rollback()

    assert store == {}
