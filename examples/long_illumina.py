from datetime import datetime, timedelta
from typing import Sequence
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import INTEGER
from ml_warehouse.ml_warehouse_schema import (
    IseqFlowcell,
    IseqProductMetrics,
    IseqRunStatus,
    IseqRunStatusDict,
    Study,
)


def summarize_long_illumina(
    sess: Session,
    faculty_sponsor_pattern: str,
    max_age: datetime,
    active_run_min_age: timedelta,
    min_tot_days: int,
    ids_also_included: Sequence[int],
) -> Query:
    """
    Get a summary of long running Illumina runs within a specific group this year.

    Arguments
    ---------
    sess: Session
        The Session to perform the query against.
    faculty_sponsor_pattern: str
        A SQL pattern string, to select the faculty_sponsor (e.g. "%bob%")
    max_age: datetime
        The age of the oldest run to consider.
    active_run_min_age: datetime
        The minimum age to consider still active runs.
    ids_also_included:
        Run IDs to include in the results regardless.

    Returns
    -------
    Query
        The Query corresponding to the search.
        When executed, each row will contain the following fields:
            id_run
            current_state
            date
            tot_days
            studies

    Corresponds to the following example SQL:
    ```sql
    SELECT
        irs.id_run,
        irsd.description current_state,
        irs.date,
        DATEDIFF(irs.date, irps.pending_date) tot_days,
        GROUP_CONCAT(DISTINCT study.name) studies
    FROM
        study
        JOIN iseq_flowcell USING(id_study_tmp)
        JOIN iseq_product_metrics ipm USING(id_iseq_flowcell_tmp)
        JOIN (
            SELECT
                MIN(date) pending_date,
                id_run
            FROM
                iseq_run_status
            WHERE
                id_run_status_dict = 1
            GROUP BY
                id_run
        ) irps USING(id_run)
        JOIN iseq_run_status irs ON irs.id_run = ipm.id_run
        AND iscurrent = 1
        JOIN iseq_run_status_dict irsd USING(id_run_status_dict)
    WHERE
        study.faculty_sponsor LIKE '%adams%'
    GROUP BY
        irs.id_run
    HAVING
        (
            description NOT IN(
                "qc complete",
                "archival complete",
                "analysis cancelled"
            )
            AND date < (NOW() - INTERVAL 2 DAY)
        )
        OR (
            tot_days > 14
            AND date > (NOW() - INTERVAL 1 year)
        )
        OR id_run IN (39927, 39960, 39961, 38675, 38738, 38739);
    ```
    """

    irps = (
        sess.query(
            func.min(IseqRunStatus.date).label("pending_date"), IseqRunStatus.id_run
        )
        .filter(IseqRunStatus.id_run_status_dict == 1)
        .group_by(IseqRunStatus.id_run)
        .subquery("irps")
    )

    tot_days = func.datediff(IseqRunStatus.date, irps.c.pending_date).label("tot_days")

    return (
        sess.query(
            IseqRunStatus.id_run,
            IseqRunStatusDict.description.label("current_state"),
            IseqRunStatus.date,
            tot_days.label("tot_days"),
            func.group_concat(func.distinct(Study.name)).label("studies"),
        )
        .join(IseqFlowcell, IseqFlowcell.id_study_tmp == Study.id_study_tmp)
        .join(
            IseqProductMetrics,
            IseqProductMetrics.id_iseq_flowcell_tmp
            == IseqFlowcell.id_iseq_flowcell_tmp,
        )
        .join(irps, irps.c.id_run == IseqProductMetrics.id_run)
        .join(
            IseqRunStatus,
            (IseqRunStatus.id_run == IseqProductMetrics.id_run)
            & (IseqRunStatus.iscurrent == 1),
        )
        .join(
            IseqRunStatusDict,
            IseqRunStatusDict.id_run_status_dict == IseqRunStatus.id_run_status_dict,
        )
        .filter(Study.faculty_sponsor.like(faculty_sponsor_pattern))
        .group_by(IseqRunStatus.id_run)
        .having(
            (
                (
                    ~(
                        IseqRunStatusDict.description.in_(
                            ("qc complete", "archival complete", "analysis cancelled")
                        )
                    )
                )
                & (IseqRunStatus.date < (active_run_min_age))
            )
            | (
                (Column(INTEGER, name="tot_days") > min_tot_days)
                & (IseqRunStatus.date > (max_age))
            )
            | (IseqRunStatus.id_run.in_(ids_also_included))
        )
    )
