from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///development.sqlite"
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string, echo=False)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        make_session = sessionmaker(bind=self.__engine)
        self.session = make_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
