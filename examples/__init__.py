import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.orm.session import Session


def get_session() -> Session:
    """
    Create a Session to connect to the MLWarehouse.

    The following environment variables must be set:
        - MYSQL_PW
        - MYSQL_USER
        - MYSQL_HOST
        - MYSQL_PORT
        - MYSQL_DBNAME
    """
    PW = os.environ["MYSQL_PW"]
    USER = os.environ["MYSQL_USER"]
    HOST = os.environ["MYSQL_HOST"]
    PORT = os.environ["MYSQL_PORT"]
    DBNAME = os.environ["MYSQL_DBNAME"]

    url = "mysql+pymysql://{user}:{passw}@{host}:{port}/{db}?charset=utf8mb4".format(
        user=USER, passw=PW, host=HOST, port=PORT, db=DBNAME
    )

    engine = create_engine(url, future=True)

    session_maker = sessionmaker(bind=engine)
    sess = session_maker()

    return sess


def print_results(query: Query, limit: int):
    """Print the first results to stdout, up to a certain limit."""

    for i, row in enumerate(query.limit(limit).all()):
        print(f"Row #{i}")

        for key, value in row._asdict().items():
            print(f"{key}: {value}")

        print()
