from src.infra.config.connection import DBConnectionHandler
from src.infra.config.base import Base
from src.infra.model.tweet import Tweet

# from src.infra.configs.base import Base


def create_tables():
    # Criar a tabela no banco de dados
    db_hadler = DBConnectionHandler()
    Base.metadata.create_all(db_hadler.get_engine())


if __name__ == "__main__":
    create_tables()
