import os
from typing import Union
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException

from src.infra.config.start_db import create_tables
from src.infra.crowler.direct_search import DirectSearchCrawler
from src.infra.crowler.authenticator import TwitterAuthenticator

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search/{subject}")
def search_subject(subject: str):
    sqlite_file = "development.sqlite"
    if os.path.isfile(sqlite_file):
        os.remove(sqlite_file)
    create_tables()

    dsc = DirectSearchCrawler()
    try:
        return dsc.search(subject, pages=3, headless=False)
    except:
        raise HTTPException(status_code=403, detail="Arquivo de autenticação ausente")


from pydantic import BaseModel


class Credentials(BaseModel):
    user: str
    email: str
    password: str


@app.post("/auth/")
async def create_item(credentials: Credentials):
    email = credentials.email
    user = credentials.user
    password = credentials.password

    session = TwitterAuthenticator(email, user, password)
    state = session.autenticate(auto=True)

    return state
