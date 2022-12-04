import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..')
sys.path.append(mymodule_dir)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from main import app
from database.db import Base, get_db
from typing import Any, Generator
from routes.questionRoutes import question_router
from routes.userRoutes import user_router
from sqlalchemy.orm import Session
from tests.users import authentication_token_from_email

def start_application():
    app = FastAPI()
    app.include_router(user_router, prefix="/users")
    app.include_router(question_router, prefix="/questions")
    return app

DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client, email="admin@gmail.com", db=db_session
    )