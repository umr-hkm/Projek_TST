import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..')
sys.path.append(mymodule_dir)

from sqlalchemy.orm import Session
from models.userModels import UserSchema
from fastapi.testclient import TestClient
from controllers.userControllers import sign_up

def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/users/signin", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    password = "password"
    user_in_create = UserSchema(
            nama="Tes User", email=email, password=password)
    user = sign_up(request=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
