from typing import List, Optional

from pytest import mark as m
import pytest
import sqlalchemy
import ml_warehouse
from ml_warehouse import *

from tests.ml_warehouse_fixture import mlwh_session, prod_session
from ml_warehouse.ml_warehouse_schema import Study, OseqFlowcell
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import Table


# Stop IDEs "optimizing" away these imports
_ = mlwh_session, prod_session


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


@m.describe("Deleting rows from the database")
class TestMLWarehouseDeleteRow(object):
    @m.it("Successfully deletes rows from the database")
    def test_delete_rows(self, mlwh_session: Session):

        study_z = mlwh_session.query(Study).filter(Study.name == "Study Z").first()

        mlwh_session.query(OseqFlowcell).filter(OseqFlowcell.study == study_z).delete()
        mlwh_session.commit()

        assert (
            mlwh_session.query(OseqFlowcell)
            .filter(OseqFlowcell.study == study_z)
            .count()
            == 0
        )


@m.describe("Test all tables in the database")
class TestMLWarehouseAllTables(object):
    @m.it("Compares model against database.")
    def test_all_tables(self, prod_session: Optional[Session]):

        if prod_session is None:
            pytest.skip("DB credentials not provided")

        engine = prod_session.connection().engine

        insp: Inspector = inspect(engine)

        table_names = insp.get_table_names()
        tables = []

        for attr in dir(ml_warehouse.ml_warehouse_schema):
            try:
                class_ = getattr(ml_warehouse.ml_warehouse_schema, attr)
                if class_.__dict__.get("__tablename__") in table_names:
                    tables.append(class_)
                elif class_.__dict__.get("name") in table_names:
                    tables.append(class_)
                    pass
            except AttributeError:
                continue

        session = Session(engine)

        for cls in tables:
            session.query(cls).limit(100).count()

        assert len(tables) == len(table_names)

        session.close()

    @m.it("Compares generated schema against prod schema")
    def test_schema_difference(
        self, prod_session: Optional[Session], mlwh_session: Session
    ):

        if prod_session is None:
            pytest.skip("DB credentials not provided")

        insp: Inspector = inspect(prod_session.connection().engine)

        table_names = insp.get_table_names()
        tables = []

        for attr in dir(ml_warehouse.ml_warehouse_schema):
            try:
                class_ = getattr(ml_warehouse.ml_warehouse_schema, attr)
                if class_.__dict__.get("__tablename__") in table_names:
                    tables.append(class_)
                elif class_.__dict__.get("name") in table_names:
                    tables.append(class_)
                    pass
            except AttributeError:
                continue

        for table in tables:

            # Get reflected and generated columns
            if isinstance(table, Table):
                refl_cols: List[dict] = insp.get_columns(table.name)
                gen_cols = table.columns

            else:
                refl_cols = insp.get_columns(table.__tablename__)
                gen_cols = dict()

                for key in dir(table):
                    attr = getattr(table, key)
                    if isinstance(
                        attr, sqlalchemy.orm.attributes.InstrumentedAttribute
                    ):

                        try:
                            gen_cols[attr.expression.name] = attr.expression
                        except:
                            pass

            for column in refl_cols:

                colname = column["name"]
                generated_column = gen_cols.get(colname)

                for (key, value) in column.items():

                    if key == "type":
                        dialect = prod_session.connection().engine.dialect
                        new_type = getattr(generated_column, key).compile(dialect)
                        new_value = value.compile(dialect)

                        assert (
                            new_type == new_value
                            or "UNSIGNED" in new_value
                            or "COLLATE" in new_value
                            or "FLOAT" in new_value
                            and new_value.split(",")[0] == new_type[:-1]
                        )
