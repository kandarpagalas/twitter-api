import os
import json
from time import sleep
from random import randint
import pandas as pd

from playwright.sync_api import sync_playwright



class Authenticator:
    def __init__(self, email, user, password, session=None) -> None:
        if session is None:
            self.session = f"src/.session/{user}.json"
        else:
            self.session = f"src/.session/{session}.json"

        self.email = email
        self.user = user
        self.password = password

    def autenticate(self, headless=False):
        with sync_playwright() as p:
            twitter_home = "https://twitter.com"

            # Abre navegador
            browser = p.chromium.launch(headless=headless)

            # Abre aba anônima
            if os.path.isfile(self.session):
                # Create a new context with the saved storage state.
                context = browser.new_context(storage_state=self.session)
                page = context.new_page()
                page.goto(twitter_home, timeout=120000)

            else:
                context = browser.new_context()
                page = context.new_page()

                # Navega até a página
                page.goto(twitter_home, timeout=60000)

                page.locator("xpath=//a[@href='/login']").click()
                sleep(3)
                input("Continue?")

                page.locator("[name='text']").fill(self.user)
                sleep(1)
                page.get_by_text("Next").click()
                sleep(5)
                input("Continue?")

                ## Adicionar etapa nome de usuário

                page.locator("[name='password']").fill(self.password)
                sleep(1)
                page.get_by_text("Log in").click()
                sleep(3)
                input("Continue?")

                # Save storage state into the file.
                context.storage_state(path=self.session)
        return self.session

    


if __name__ == "__main__":
    email = os.environ["TWITTER_USER"]
    user = os.environ["TWITTER_USER"]
    password = os.environ["TWITTER_PASSWORD"]

    session = Authenticator(email, user, password)
    state = session.autenticate()


    # dsc = DirectSearchCrawler(email, user, password)
    # dsc.search("homelab", pages=3, headless=False)
    # df = dsc.to_pandas()
    # df.to_csv("tweets_v2.csv")

    print(state)
