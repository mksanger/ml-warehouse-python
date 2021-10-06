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

from typing import Optional
from ml_warehouse.ml_warehouse_schema import BmapFlowcell, PacBioRun, StockResource
from sqlalchemy.orm import Session, Query


def get_stock_records(sess: Session, stock_id: str):
    """Get StockResource records by stock ID.

    Arguments
    ---------
    sess: Session
        The Session to perform the query against.
    stock_id: str
        The stock ID for the StockResource.

    Returns
    -------
    Query
        The Query corresponding to the search.

    Equivalent to the following:
        ```
        my @stock_records = $self->mlwh_schema->resultset('StockResource')->search
            ({id_stock_resource_lims => $stock_id},
            {prefetch               => ['sample', 'study']});
        ```

    """

    result = sess.query(StockResource).filter(
        StockResource.id_stock_resource_lims == stock_id
    )

    return result


def get_bmap_flowcell_records(sess: Session, chip_serialnumber: str, position: int):
    """Get BmapFlowcell records by chip serialnumber and flowcell position.

    Arguments
    ---------
    sess: Session
        The Session to perform the query against.
    chip_serialnumber: str
        The chip serialnumber.
    position: int
        The BmapFlowcell position.

    Returns
    -------
    Query
        The Query object corresponding to the search.

    Equivalent to the following:
        ```
        my @flowcell_records = $self->mlwh_schema->resultset('BmapFlowcell')->search
            ({chip_serialnumber => $chip_serialnumber,
            position          => $position},
            {prefetch => ['sample', 'study']});
        ```
    """

    result = sess.query(BmapFlowcell).filter(
        (BmapFlowcell.chip_serialnumber == chip_serialnumber)
        & (BmapFlowcell.position == position)
    )

    return result


def find_pacbio_runs(
    sess: Session, run_id: str, plate_well: str, tag_identifier: Optional[str] = None
) -> Query:
    """Find run records for a PacBio run ID.

    Arguments
    ---------
    sess: Session
        The Session to perform the query on.
    run_id: str
        PacBio run ID.
    plate_well: str
        PacBio plate well, zero-padded form.
    tag_identifier: Optional[str]
        Tag identifier.

    Returns
    -------
    Query
        The Query object corresponding to the search.
    """

    result = sess.query(PacBioRun).filter(
        (PacBioRun.pac_bio_run_name == run_id) | (PacBioRun.well_label == plate_well)
    )

    if tag_identifier is not None:
        result = result.filter(PacBioRun.tag_identifier == tag_identifier)

    return result.group_by(
        PacBioRun.pac_bio_run_name, PacBioRun.well_label, PacBioRun.tag_identifier
    )
