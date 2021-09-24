from datetime import datetime

from ml_warehouse.ml_warehouse_schema import (
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
