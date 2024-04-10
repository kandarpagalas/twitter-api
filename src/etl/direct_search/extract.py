import json
from datetime import datetime
from src.infra.repository.tweet_repository import TweetRepository


class TweetsExtractor:
    def __init__(self, _data: dict) -> None:
        try:
            timeline = _data["data"]["search_by_raw_query"]["search_timeline"][
                "timeline"
            ]
            # Tweets
            self.__entries = timeline["instructions"][0]["entries"]
            # Feedbacks
            # responseObjects = timeline["responseObjects"]
        except Exception as e:
            self.__entries = []
            print(e)

    def to_list(self):
        dataset = []
        for entry in self.__entries:
            try:
                # tweet = Tweet(data)
                tr = TweetRepository()
                tweet = tr.transform_insert(entry)

                # tweet = TweetDataParser(entry)
                dataset.append(tweet)
            except Exception as e:
                pass
        return dataset


# class TweetDataParser:
#     def __init__(self, entry_data: dict):
#         content = entry_data["content"]["itemContent"]["tweet_results"]["result"]
#         # Tweet data
#         legacy = content["legacy"]
#         entities = legacy["entities"]
#         # User Data
#         core = content["core"]["user_results"]["result"]
#         core_legacy = core["legacy"]

#         # User
#         self.acc_id = core["rest_id"]
#         self.acc_is_blue_verified = core["is_blue_verified"]

#         date_format = "%a %b %d %H:%M:%S %z %Y"
#         self.acc_created_at = datetime.strptime(core_legacy["created_at"], date_format)
#         self.acc_followers_count = core_legacy["followers_count"]
#         self.acc_location = core_legacy["location"]
#         self.acc_name = core_legacy["name"]
#         self.acc_screen_name = core_legacy["screen_name"]

#         # Tweet
#         self.tweet_id = legacy["id_str"]
#         self.tweet_user_id = legacy["user_id_str"]
#         self.tweet_full_text = legacy["full_text"].replace("\n", " ")
#         self.tweet_lang = legacy["lang"]
#         self.tweet_hastags = str(list(map(lambda x: x["text"], entities["hashtags"])))

#     def data(self):
#         return self.__dict__

#     def __repr__(self) -> str:
#         return str(self.__dict__)


if __name__ == "__main__":
    import os
    import pandas as pd
    from src.infra.config.start_db import create_tables

    if os.path.isfile("development.sqlite"):
        os.remove("development.sqlite")
        create_tables()

    with open("data/entry_33.json", "r", encoding="utf-8") as f:
        raw_data = json.loads(f.read())
        try:
            tweets = TweetsExtractor(raw_data)
            df = pd.DataFrame(tweets.to_list())
            print(df)
        except:
            pass

        # print(tweet.__dict__)
