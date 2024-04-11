import os
from typing import Union
from dotenv import load_dotenv


from flask import Flask, request, render_template

from src.infra.config.start_db import create_tables
from src.infra.crowler.direct_search import DirectSearchCrawler

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/page/<int:page_num>")
def page(page_num):
    return render_template("page" + str(page_num) + ".html")


@app.route("/post_message", methods=["POST"])
def post_message(page_num):
    senha = request.form.get("senha")
    password = request.form.get("password")
    return render_template("page" + str(page_num) + ".html")


@app.route("/search/<str:subject>")
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


if __name__ == "__main__":
    app.run(debug=True)
