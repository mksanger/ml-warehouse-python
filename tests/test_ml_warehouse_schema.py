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

from typing import List, Optional

import pytest
import sqlalchemy
from pytest import mark as m
from sqlalchemy import Table, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

import ml_warehouse
from ml_warehouse.schema import OseqFlowcell, Study


@m.describe("Querying the ML Warehouse")
class TestMLWarehouseQueries(object):
    @m.it("Successfully retrieves records of study")
    def test_retrieve_study(self, mlwh_session):

        all_studies = mlwh_session.query(Study).all()

        assert len(all_studies) > 0


@m.describe("Resilience to modifying the database schema")
class TestMLWarehouseResilience(object):
    @m.it("Retrieves a record of study after a column is added")
    def test_added_column_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE study ADD COLUMN extra_column INT;")
        mlwh_session.commit()

        studies = mlwh_session.query(Study).all()

        assert len(studies) > 0

    @m.it("Retrieves records after column type has been extended")
    def test_extended_column_type_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE oseq_flowcell MODIFY instrument_slot BIGINT;")
        mlwh_session.commit()

        oseq_flowcells = mlwh_session.query(OseqFlowcell).all()

        assert len(oseq_flowcells) > 0

    @m.it("Fails to retrieve records after a column has been dropped")
    @m.xfail(raises=sqlalchemy.exc.OperationalError, strict=True)
    def test_dropped_column_resilience(self, mlwh_session: Session):

        mlwh_session.execute("ALTER TABLE study DROP COLUMN name;")
        mlwh_session.commit()

        studies = mlwh_session.query(Study).all()

        assert len(studies) > 0


@m.describe("Deleting rows from the database")
class TestMLWarehouseDeleteRow(object):
    @m.it("Deletes rows from the database")
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
    def test_all_tables(self, prod_session: Optional[Session], mlwh_session):

        if prod_session is None:
            pytest.skip("DB credentials not provided")

        engine = prod_session.connection().engine

        insp: Inspector = inspect(engine)

        table_names = insp.get_table_names()
        tables = []

        for attr in dir(ml_warehouse.schema):
            try:
                class_ = getattr(ml_warehouse.schema, attr)
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

        insp: Inspector = inspect(prod_session.connection())

        table_names = insp.get_table_names()
        tables = []

        for attr in dir(ml_warehouse.schema):
            try:
                class_ = getattr(ml_warehouse.schema, attr)
                if class_.__dict__.get("__tablename__") in table_names:
                    tables.append(class_)
                elif class_.__dict__.get("name") in table_names:
                    tables.append(class_)
                    pass
            except AttributeError:
                continue

        for table in tables:

            if isinstance(table, DeclarativeMeta):
                table: Table = table.__table__

            # Get reflected and generated columns
            refl_cols: List[dict] = insp.get_columns(table.name)
            gen_cols = table.columns

            for column in refl_cols:

                colname = column["name"]
                generated_column = gen_cols.get(colname)

                # Check reflected column type against generated column type
                dialect = prod_session.connection().engine.dialect
                refl_type = column["type"].compile(dialect)
                gen_type = generated_column.type.compile(dialect)

                # Exception for known inconsistency in the schema
                assert (
                    refl_type == gen_type
                    or table.name in ["iseq_external_product_components"]
                    and colname in ["id_iseq_product_ext"]
                )

            # Check all primary keys
            table_name = table.name

            refl_pks = set(insp.get_pk_constraint(table_name)["constrained_columns"])
            gen_pks = {col.name for col in table.primary_key.columns}

            assert refl_pks == gen_pks

            # Check all foreign keys
            refl_fks: list = insp.get_foreign_keys(table_name)
            expanded_refl_fks = list()
            gen_fks = table.foreign_keys

            for f in refl_fks:
                # assert f["constrained_columns"] == f["referred_columns"]
                for cons, refd in zip(f["constrained_columns"], f["referred_columns"]):
                    new_dict = f
                    new_dict["constrained_columns"] = cons
                    new_dict["referred_columns"] = refd
                    expanded_refl_fks.append(new_dict)

            assert len(expanded_refl_fks) == len(gen_fks)

            # Check the foreign keys

            for foreign_key in expanded_refl_fks:

                corresponding_generated = list(
                    filter(
                        lambda f: f.column.table.name == foreign_key["referred_table"]
                        and f.column.name == foreign_key["referred_columns"]
                        and f.parent.name == foreign_key["constrained_columns"],
                        gen_fks,
                    )
                )

                assert len(corresponding_generated) == 1
                corresponding_generated = corresponding_generated[0]

                for opt, value in foreign_key["options"].items():
                    assert value == getattr(corresponding_generated, opt)
