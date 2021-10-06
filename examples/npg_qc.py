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

from typing import Sequence

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from ml_warehouse.ml_warehouse_schema import (
    IseqFlowcell,
    IseqProductMetrics,
    IseqRunLaneMetrics,
    Study,
)

from sqlalchemy.sql.expression import distinct
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func


def get_iseq_product_metrics_run(
    sess: Session, run_ids: Sequence[int], excluded_type: str, study_count: int
):
    """
    Get IseqProductMetrics run IDs and Study count given certain constraints.

    Arguments
    ---------
    sess: Session
        The Session to perform the query against.
    run_ids: Sequence[int]
        The run IDs to check.
    excluded_type: str
        The Flowcell type to exclude from the search.
    study_count: int
        The study count that IseqProductMetrics should match.

    Returns
    -------
    Query
        The Query object corresponding to the search.


    Equivalent to the following:
        my $query =
            q[select p.id_run, count(distinct s.id_study_lims) as study_count ] .
            q[from iseq_product_metrics p ] .
            q[join iseq_flowcell f on p.id_iseq_flowcell_tmp=f.id_iseq_flowcell_tmp ] .
            q[join study s on s.id_study_tmp=f.id_study_tmp ] .
            qq[where f.entity_type != ? and p.id_run in (${placeholders}) ] .
            q[group by p.id_run having study_count = ?];
    """

    study_count_f = func.count(distinct(Study.id_study_lims))

    return (
        sess.query(IseqProductMetrics.id_run, study_count_f.label("study_count"))
        .join(IseqProductMetrics.iseq_flowcell)
        .join(IseqFlowcell.study)
        .filter(
            ~(IseqFlowcell.entity_type == excluded_type)
            & (IseqProductMetrics.id_run.in_(run_ids))
        )
        .group_by(IseqProductMetrics.id_run)
        .having(Column(Integer, name="study_count") == study_count)
    )


def get_iseq_product_metrics_by_study(
    sess: Session, study_name: str, run_ids: Sequence[int]
):
    """
    Get IseqProductMetrics run IDs from a set, given a study name.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    study_name: str
        The Study name to match against.
    run_ids: Sequence[int]
        The set of run IDs to search within.

    Returns
    -------
    Query
        The Query corresponding to the search.

    Equivalent to the following:
        ```
        $query =
            q[select distinct p.id_run from iseq_product_metrics p join iseq_flowcell f ] .
            q[on p.id_iseq_flowcell_tmp=f.id_iseq_flowcell_tmp ] .
            q[join study s on s.id_study_tmp=f.id_study_tmp ] .
            qq[where s.name = ? and p.id_run in (${placeholders})];
        ```
    """

    result = (
        sess.query(IseqProductMetrics.id_run)
        .distinct()
        .join(IseqProductMetrics.iseq_flowcell)
        .join(IseqFlowcell.study)
        .filter((Study.name == study_name) & (IseqProductMetrics.id_run.in_(run_ids)))
    )

    return result


def get_iseq_product_metrics_by_decode_percent(
    sess: Session, max_decode_percent: int, run_ids: Sequence[int]
):
    """
    Get IseqRunLaneMetrics run IDs from a set within a maximum tags_decode_percent.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    max_decode_percent: int
        The maximum desired tags_decode_percent.
    run_ids: Sequence[int]
        The set of run IDs against which to perform the search.

    Returns
    -------
    Query
        The Query corresponding to the search.

    Equivalent to the following:
        ```
        $query =
            q[select distinct(id_run) from iseq_run_lane_metrics ] .
            q[where (tags_decode_percent is null or tags_decode_percent < ?) ] .
            qq[and id_run in (${placeholders})];
        ```
    """

    result = (
        sess.query(IseqRunLaneMetrics.id_run)
        .distinct()
        .filter(
            (
                (IseqRunLaneMetrics.tags_decode_percent == None)
                | (IseqRunLaneMetrics.tags_decode_percent < max_decode_percent)
            )
            & (IseqRunLaneMetrics.id_run.in_(run_ids))
        )
    )

    return result
