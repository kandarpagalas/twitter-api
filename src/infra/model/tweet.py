from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.infra.config.base import Base


class Tweet(Base):
    __tablename__ = "tweets"  # obrigatório

    tweet_id = Column(Integer, primary_key=True)
    tweet_user_id = Column(Integer, nullable=False)
    tweet_full_text = Column(String, nullable=False)
    tweet_lang = Column(String, nullable=False)
    tweet_hastags = Column(String, nullable=False)

    acc_id = Column(Integer, nullable=False)
    acc_is_blue_verified = Column(Boolean, nullable=False)
    acc_created_at = Column(DateTime, nullable=False)
    acc_followers_count = Column(Integer, nullable=False)
    acc_location = Column(String, nullable=False)
    acc_name = Column(String, nullable=False)
    acc_screen_name = Column(String, nullable=False)
