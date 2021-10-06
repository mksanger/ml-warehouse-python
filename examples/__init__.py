# -*- coding: utf-8 -*-
#
# Copyright © 2021 Genome Research Ltd. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @author Adam Blanchet <ab59@sanger.ac.uk>

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
