import os
import re
import json
from time import sleep
from random import randint
import pandas as pd

from playwright.sync_api import sync_playwright


class TwitterAuthenticator:
    def __init__(self, email=None, user=None, password=None, session=None) -> None:
        if session is None:
            self.session = f"src/.session/{user}.json"
        else:
            self.session = f"src/.session/{session}.json"

        self.email = email
        self.user = user
        self.password = password

    def autenticate(self, auto=False, headless=False):
        # Setup the handler.

        with sync_playwright() as p:
            twitter_home = "https://twitter.com"

            # Abre navegador
            browser = p.chromium.launch(headless=headless)

            # Abre aba anônima
            context = browser.new_context()
            page = context.new_page()

            # Navega até a página
            page.goto(twitter_home, timeout=60000)

            page.locator("xpath=//a[@href='/login']").click()
            sleep(2)

            if auto:
                page.locator("[name='text']").fill(self.email)
                sleep(1)
                page.get_by_text("Next").click()
                sleep(2)

                try:
                    page.locator("[name='text']").fill(self.user)
                    sleep(1)
                    page.get_by_text("Next").click()
                    sleep(2)
                except Exception as e:
                    print(e)

                page.locator("[name='password']").fill(self.password)
                sleep(1)
                page.get_by_text("Log in").click()
                sleep(2)
            # else:
            #     input("Salvar estado?")

            page.get_by_text("For You").click()

            # Save storage state into the file.
            context.storage_state(path=self.session)

        return self.session


if __name__ == "__main__":
    email = os.environ["TWITTER_EMAIL"]
    user = os.environ["TWITTER_USER"]
    password = os.environ["TWITTER_PASSWORD"]

    session = TwitterAuthenticator(email, user, password)
    state = session.autenticate(auto=True)

    # dsc = DirectSearchCrawler(email, user, password)
    # dsc.search("homelab", pages=3, headless=False)
    # df = dsc.to_pandas()
    # df.to_csv("tweets_v2.csv")

    print(state)
