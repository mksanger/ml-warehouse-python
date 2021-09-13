from pytest import mark as m
import sqlalchemy

from tests.ml_warehouse_fixture import mlwh_session
from ml_warehouse.ml_warehouse_schema import Study, OseqFlowcell
from sqlalchemy.orm import Session

# Stop IDEs "optimizing" away this import
_ = mlwh_session


@m.describe("Querying the ML Warehouse")
class TestMLWarehouseQueries(object):
    @m.it("Successfully retrieves records of study")
    def test_retrieve_study(self, mlwh_session):

        all_studies = mlwh_session.query(Study).all()

        assert len(all_studies) > 0


@m.describe("Resilience to modifiying the database schema")
class TestMLWarehouseResilience(object):
    @m.it("Successfully retrieves a record of study after a column is added")
    def test_added_column_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE study ADD COLUMN extra_column INT;")
        mlwh_session.commit()

        studies = mlwh_session.query(Study).all()

        assert len(studies) > 0

    @m.it("Successfully retrieves records after column type has been extended")
    def test_extended_column_type_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE oseq_flowcell MODIFY instrument_slot BIGINT;")
        mlwh_session.commit()

        oseq_flowcells = mlwh_session.query(OseqFlowcell).all()

        assert len(oseq_flowcells) > 0

    @m.it("Fail to retreive records after a column has been dropped")
    @m.xfail(raises=sqlalchemy.exc.OperationalError, strict=True)
    def test_dropped_column_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE study DROP COLUMN name;")
        mlwh_session.commit()

        studies = mlwh_session.query(Study).all()

        assert len(studies) > 0
