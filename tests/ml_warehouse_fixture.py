from configparser import ConfigParser, Error
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils.functions.database import drop_database
from sqlalchemy import func

from ml_warehouse.ml_warehouse_schema_new import Base, OseqFlowcell, Sample, Study

EARLY = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
LATE = datetime(year=2020, month=6, day=14, hour=0, minute=0, second=0)
LATEST = datetime(year=2020, month=6, day=30, hour=0, minute=0, second=0)


def initialize_mlwh(session: Session):
    instrument_name = "instrument_01"
    pipeline_id_lims = "Ligation"
    req_data_type = "Basecalls and raw data"

    study_x = Study(
        id_lims="LIMS_01",
        id_study_lims="study_01",
        name="Study X",
        last_updated=func.now(),
        recorded_at=func.now(),
    )
    study_y = Study(
        id_lims="LIMS_01",
        id_study_lims="study_02",
        name="Study Y",
        last_updated=func.now(),
        recorded_at=func.now(),
    )
    study_z = Study(
        id_lims="LIMS_01",
        id_study_lims="study_03",
        name="Study Z",
        last_updated=func.now(),
        recorded_at=func.now(),
    )
    session.add_all([study_x, study_y, study_z])
    session.flush()

    samples = []
    flowcells = []

    num_samples = 200
    for s in range(1, num_samples + 1):
        sid = "sample{}".format(s)
        name = "sample {}".format(s)
        samples.append(
            Sample(
                id_lims="LIMS_01",
                id_sample_lims=sid,
                name=name,
                last_updated=func.now(),
                recorded_at=func.now(),
            )
        )
    session.add_all(samples)
    session.flush()

    num_simple_expts = 5
    num_instrument_pos = 5
    sample_idx = 0
    for expt in range(1, num_simple_expts + 1):
        for pos in range(1, num_instrument_pos + 1):
            expt_name = "simple_experiment_{:03}".format(expt)
            id_flowcell = "flowcell{:03}".format(pos + 10)

            # All the even experiments have the early datetime
            # All the odd experiments have the late datetime
            when_expt = EARLY if expt % 2 == 0 else LATE

            flowcells.append(
                OseqFlowcell(
                    sample=samples[sample_idx],
                    study=study_y,
                    instrument_name=instrument_name,
                    instrument_slot=pos,
                    experiment_name=expt_name,
                    id_flowcell_lims=id_flowcell,
                    pipeline_id_lims=pipeline_id_lims,
                    requested_data_type=req_data_type,
                    last_updated=when_expt,
                    recorded_at=when_expt,
                    id_lims="SEQSCAPE",
                )
            )
            sample_idx += 1

    num_multiplexed_expts = 3
    num_instrument_pos = 5
    barcodes = [
        "CACAAAGACACCGACAACTTTCTT",
        "ACAGACGACTACAAACGGAATCGA",
        "CCTGGTAACTGGGACACAAGACTC",
        "TAGGGAAACACGATAGAATCCGAA",
        "AAGGTTACACAAACCCTGGACAAG",
        "GACTACTTTCTGCCTTTGCGAGAA",
        "AAGGATTCATTCCCACGGTAACAC",
        "ACGTAACTTGGTTTGTTCCCTGAA",
        "AACCAAGACTCGCTGTGCCTAGTT",
        "GAGAGGACAAAGGTTTCAACGCTT",
        "TCCATTCCCTCCGATAGATGAAAC",
        "TCCGATTCTGCTTCTTTCTACCTG",
    ]

    msample_idx = 0
    for expt in range(1, num_multiplexed_expts + 1):
        for pos in range(1, num_instrument_pos + 1):
            expt_name = "multiplexed_experiment_{:03}".format(expt)
            id_flowcell = "flowcell{:03}".format(pos + 100)

            # All the even experiments have the early datetime
            when = EARLY

            # All the odd experiments have the late datetime
            if expt % 2 == 1:
                when = LATE
                # Or latest if they have an odd instrument position
                if pos % 2 == 1:
                    when = LATEST

            for barcode_idx, barcode in enumerate(barcodes):
                tag_id = "ONT_EXP-012-{:02d}".format(barcode_idx + 1)

                flowcells.append(
                    OseqFlowcell(
                        sample=samples[msample_idx],
                        study=study_z,
                        instrument_name=instrument_name,
                        instrument_slot=pos,
                        experiment_name=expt_name,
                        id_flowcell_lims=id_flowcell,
                        tag_set_id_lims="ONT_12",
                        tag_set_name="ONT library barcodes x12",
                        tag_sequence=barcode,
                        tag_identifier=tag_id,
                        pipeline_id_lims=pipeline_id_lims,
                        requested_data_type=req_data_type,
                        last_updated=when,
                        recorded_at=when,
                        id_lims="SEQSCAPE",
                    )
                )
                msample_idx += 1

    session.add_all(flowcells)
    session.commit()


@pytest.fixture(scope="function")
def mlwh_session(config) -> Session:

    uri = mysql_url(config)
    # uri = "sqlite:///mlwh.db"
    engine = create_engine(uri, echo=False)

    if not database_exists(engine.url):
        create_database(engine.url)

    # Workaround for invalid default values for dates.
    engine.execute("SET sql_mode = '';")

    Base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)
    sess = session_maker()

    initialize_mlwh(sess)

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

    return "mysql+pymysql://{}:{}@{}:{}/{}".format(
        user, password, ip_address, port, schema
    )
