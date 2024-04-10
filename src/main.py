import os
from typing import Union
from dotenv import load_dotenv

from fastapi import FastAPI

from src.infra.config.start_db import create_tables
from src.infra.crowler.direct_search import DirectSearchCrawler

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

    # if not os.path.isfile("development.sqlite"):
    #     create_tables()
    #     print("Criando tabelas no banco de dados")

    load_dotenv()
    email = os.environ["TWITTER_USER"]
    user = os.environ["TWITTER_USER"]
    password = os.environ["TWITTER_PASSWORD"]

    dsc = DirectSearchCrawler(email, user, password)
    dsc.search(subject, pages=3, headless=False)
    # df = dsc.to_pandas()
    # df.to_csv("tweets_v2.csv")

    return dsc.get_dataset()
