import os
import json
from time import sleep
from random import shuffle
import pandas as pd

from playwright.sync_api import sync_playwright

from src.etl.direct_search.extract import TweetsExtractor


class DirectSearchCrawler:
    def __init__(self, session="src/.session/state.json") -> None:
        self.session = session
        self.dataset = []

    def _get_state_instance(self):
        files = os.listdir("src/.session/")

        states = list(filter(lambda x: ".json" in x, files))

        if len(states) == 0:
            raise Exception("Não existe state para ser usado")

        shuffle(states)

        return "src/.session/" + states.pop()

    # def autenticate(self, headless=True):
    #     with sync_playwright() as p:
    #         twitter_home = "https://twitter.com"

    #         # Abre navegador
    #         browser = p.chromium.launch(headless=headless)

    #         # Abre aba anônima
    #         if os.path.isfile(self.session):
    #             # Create a new context with the saved storage state.
    #             context = browser.new_context(storage_state=self.session)
    #             page = context.new_page()
    #             page.goto(twitter_home, timeout=120000)

    #         else:
    #             context = browser.new_context()
    #             page = context.new_page()

    #             # Navega até a página
    #             page.goto(twitter_home, timeout=60000)

    #             page.locator("xpath=//a[@href='/login']").click()
    #             sleep(3)

    #             page.locator("[name='text']").fill(self.user)
    #             sleep(1)
    #             page.get_by_text("Next").click()
    #             sleep(5)

    #             ## Adicionar etapa nome de usuário

    #             page.locator("[name='password']").fill(self.password)
    #             sleep(1)
    #             page.get_by_text("Log in").click()
    #             sleep(3)

    #             # Save storage state into the file.
    #             context.storage_state(path=self.session)

    def search(self, subject, pages=5, headless=False):
        state = self._get_state_instance()
        # if not os.path.isfile(self.session):
        #     self.autenticate()

        def handle_response_page(response):
            if "SearchTimeline" in response.url:
                try:
                    res_data = response.json()
                    tweets = TweetsExtractor(res_data)
                    self.dataset.extend(tweets.to_list())

                    # with open(
                    #     f"data/entry_{randint(0, 100)}.json", "w", encoding="utf-8"
                    # ) as f:
                    #     f.write(json.dumps(raw_data, indent=4))

                except Exception as e:
                    print(e)

        def page_scroll(page, repeat=5, interval=2):
            # page.mouse.wheel(horizontally, vertically(positive is
            # scrolling down, negative is scrolling up)
            for _ in range(repeat):  # make the range as long as needed
                page.mouse.wheel(0, 15000)
                sleep(interval)

        with sync_playwright() as p:
            twitter_home = "https://twitter.com"

            # Abre navegador
            browser = p.chromium.launch(headless=False)
            # Create a new context with the saved storage state.
            context = browser.new_context(storage_state=state)
            # Abre aba anônima
            page = context.new_page()
            # Navega até a página inicial
            page.goto(twitter_home, timeout=120000)

            page.on("response", handle_response_page)

            endpoint = f"https://twitter.com/search?q={subject}&src=typed_query"

            page.goto(endpoint, timeout=60000)
            sleep(2)

            page_scroll(page, repeat=pages)

            sleep(3)
            page.close()
            context.close()
            browser.close()

        return self.dataset

    def to_pandas(self):
        return pd.DataFrame(self.dataset)

    def get_dataset(self):
        return self.dataset


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    email = os.environ["TWITTER_USER"]
    user = os.environ["TWITTER_USER"]
    password = os.environ["TWITTER_PASSWORD"]

    dsc = DirectSearchCrawler(email, user, password)
    dsc.search("homelab", pages=3, headless=False)
    df = dsc.to_pandas()
    df.to_csv("tweets_v2.csv")

    print(df)
