from datetime import datetime
from src.infra.model.tweet import Tweet
from src.infra.repository.base_repository import BaseRepository


class TweetRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Tweet)
        self.data = {}

    def transform_insert(self, entry_data: dict):
        date_format = "%a %b %d %H:%M:%S %z %Y"

        content = entry_data["content"]["itemContent"]["tweet_results"]["result"]
        # Tweet data
        legacy = content["legacy"]
        entities = legacy["entities"]
        # User Data
        core = content["core"]["user_results"]["result"]
        core_legacy = core["legacy"]

        # User
        self.data["acc_id"] = core["rest_id"]
        self.data["acc_is_blue_verified"] = core["is_blue_verified"]

        self.data["acc_created_at"] = datetime.strptime(
            core_legacy["created_at"], date_format
        )
        self.data["acc_followers_count"] = core_legacy["followers_count"]
        self.data["acc_location"] = core_legacy["location"]
        self.data["acc_name"] = core_legacy["name"]
        self.data["acc_screen_name"] = core_legacy["screen_name"]

        # Tweet
        self.data["tweet_id"] = legacy["id_str"]
        self.data["tweet_user_id"] = legacy["user_id_str"]
        self.data["tweet_full_text"] = legacy["full_text"].replace("\n", " ")
        self.data["tweet_lang"] = legacy["lang"]
        self.data["tweet_hastags"] = str(
            list(map(lambda x: x["text"], entities["hashtags"]))
        )

        self.insert(self.data)
        return self.data
