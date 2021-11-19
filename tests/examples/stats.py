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

from datetime import datetime

from ml_warehouse.schema import (
    IseqRunLaneMetrics,
    IseqRunStatus,
    IseqRunStatusDict,
)

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func


def get_sequenced_sum(sess: Session, since: datetime):
    """
    Get number of sequenced bases each month from IseqRunLaneMetrics.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    since: datetime
        The earliest date from which to count sequencing runs.

    Returns
    -------
    Query
        The Query corresponding to the search, with fields `bases`, `month`, `count`.
    """

    return (
        sess.query(
            func.sum(
                IseqRunLaneMetrics.cycles
                * IseqRunLaneMetrics.interop_cluster_count_pf_total
            ).label("bases"),
            func.date_format(IseqRunStatus.date, "%Y-%m").label("month"),
            func.count("*").label("count"),
        )
        .filter(
            (IseqRunLaneMetrics.id_run == IseqRunStatus.id_run)
            & (IseqRunStatus.id_run_status_dict == IseqRunStatusDict.id_run_status_dict)
            & (IseqRunStatusDict.description == "qc complete")
            & (IseqRunStatus.date > since)
        )
        .group_by("month")
        .order_by("month")
    )
