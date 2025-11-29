import pytest

from backend.db import init_db


@pytest.fixture(scope="session")
def setup_test_db():
    init_db()
