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
from configparser import ConfigParser, Error
from datetime import datetime
from typing import Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils.functions.database import drop_database
import yaml

from ml_warehouse.ml_warehouse_schema import (
    Base,
    BmapFlowcell,
    FlgenPlate,
    IseqFlowcell,
    IseqProductMetrics,
    IseqRunLaneMetrics,
    IseqRunStatus,
    IseqRunStatusDict,
    OseqFlowcell,
    PacBioRun,
    Sample,
    StockResource,
    Study,
    StudyUsers,
)


def insert_from_yaml(sess: Session, table_type, fixtures_fname: str):

    with open(fixtures_fname, "r") as f:

        fixtures = yaml.safe_load(f)
        objs = []
        for row in fixtures:

            table = table_type()
            for key, value in row.items():
                setattr(table, key, value)

            objs.append(table)

        sess.add_all(objs)
        sess.commit()


def initialize_mlwh(session: Session):

    insert_from_yaml(
        session, IseqRunStatusDict, "tests/fixtures/00-IseqRunStatusDict.yml"
    )
    insert_from_yaml(session, IseqRunStatus, "tests/fixtures/100-IseqRunStatus.yml")

    insert_from_yaml(session, StudyUsers, "tests/fixtures/100-StudyUser.yml")
    insert_from_yaml(session, Sample, "tests/fixtures/200-Sample.yml")
    insert_from_yaml(session, Study, "tests/fixtures/200-Study.yml")

    insert_from_yaml(session, StockResource, "tests/fixtures/400-StockResource.yml")
    insert_from_yaml(session, OseqFlowcell, "tests/fixtures/300-OseqFlowcell.yml")

    insert_from_yaml(session, BmapFlowcell, "tests/fixtures/300-BmapFlowcell.yml")
    insert_from_yaml(session, IseqFlowcell, "tests/fixtures/300-IseqFlowcell.yml")

    insert_from_yaml(session, PacBioRun, "tests/fixtures/300-PacBioRun.yml")
    insert_from_yaml(
        session, IseqRunLaneMetrics, "tests/fixtures/400-IseqRunLaneMetric.yml"
    )


@pytest.fixture(scope="function")
def mlwh_session_flgen(mlwh_session: Session) -> Session:
    mlwh_session.execute(text("SET foreign_key_checks=0;"))
    insert_from_yaml(mlwh_session, Study, "tests/fixtures/400-Study.yml")
    insert_from_yaml(mlwh_session, Sample, "tests/fixtures/400-Sample.yml")
    insert_from_yaml(mlwh_session, FlgenPlate, "tests/fixtures/400-FlgenPlate.yml")
    mlwh_session.execute(text("SET foreign_key_checks=1;"))

    yield mlwh_session


@pytest.fixture(scope="function")
def mlwh_session_ipm(mlwh_session) -> Session:
    mlwh_session.execute(text("SET foreign_key_checks=0;"))
    insert_from_yaml(
        mlwh_session, IseqProductMetrics, "tests/fixtures/300-IseqProductMetric.yml"
    )
    mlwh_session.execute(text("SET foreign_key_checks=1;"))

    yield mlwh_session


@pytest.fixture(scope="function")
def prod_session() -> Optional[Session]:

    user = os.environ.get("MYSQL_USER")
    db = os.environ.get("MYSQL_DBNAME")
    password = os.environ.get("MYSQL_PW")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")

    if None in (user, db, password, host, port):
        yield None
        return

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
    engine = create_engine(url, future=True)
    session = Session(engine)

    yield session

    session.close()


@pytest.fixture(scope="function")
def mlwh_session(config) -> Session:

    uri = mysql_url(config)
    # uri = "sqlite:///mlwh.db"
    engine = create_engine(uri, echo=False, future=True)

    if not database_exists(engine.url):
        create_database(engine.url)

    with engine.connect() as conn:
        # Workaround for invalid default values for dates.
        conn.execute(text("SET sql_mode = '';"))
        conn.commit()
        # Make it easier to populate the tables
        conn.execute(text("SET foreign_key_checks=0;"))
        conn.commit()

    Base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)
    sess: Session() = session_maker()

    initialize_mlwh(sess)
    with engine.connect() as conn:
        conn.execute(text("SET foreign_key_checks=1;"))
        conn.commit()

    yield sess
    sess.close()

    drop_database(engine.url)


def mysql_url(config: ConfigParser):
    """Returns a MySQL URL configured through an ini file.

    The keys and values are:

    [MySQL]
    user       = <database user, defaults to "mlwh">
    password   = <database password, defaults to empty i.e. "">
    ip_address = <database IP address, defaults to "127.0.0.1">
    port       = <database port, defaults to 3306>
    schema     = <database schema, defaults to "mlwh">
    """
    section = "MySQL"

    if section not in config.sections():
        raise Error(
            "The {} configuration section is missing. "
            "You need to fill this in before running "
            "tests on a {} database".format(section, section)
        )
    connection_conf = config[section]
    user = connection_conf.get("user", "mlwh")
    password = connection_conf.get("password", "")
    ip_address = connection_conf.get("ip_address", "127.0.0.1")
    port = connection_conf.get("port", "3306")
    schema = connection_conf.get("schema", "mlwh")

    return "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        user, password, ip_address, port, schema
    )
