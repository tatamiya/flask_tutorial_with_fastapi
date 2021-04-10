import tempfile

from fastapir.main import app
from fastapir.db import crud
from fastapir.db.database import get_db, create_db_session

test_db = tempfile.NamedTemporaryFile(suffix=".db")

TestingSessionLocal = create_db_session("sqlite:///" + test_db.name)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


test_user = crud.UserCreate(
    username="test_user",
    hashed_password="$2b$12$b0QaOkAp1tGptfKqW0JRBeSu1Vn9HGHusMf7BPSEbDkGxgbz5KXWS",
)
for db in override_get_db():
    crud.create_user(db, test_user)

app.dependency_overrides[get_db] = override_get_db
