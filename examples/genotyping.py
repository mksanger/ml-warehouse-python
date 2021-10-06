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

from sqlalchemy.orm import Session
from ml_warehouse.ml_warehouse_schema import FlgenPlate


def get_flgen_plate(sess: Session, plate_barcode: int, well_label: str):
    """Get set of FlgenPlate with matching plate barcode and well label.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    plate_barcode: int
        The manufacturer (Fluidigm) barcode.
    well_label: str
        The manufacturer well identifier.

    Returns
    -------
    Query
        The Query corresponding to the search. It fields correspond to the columns of
        FlgenPlate.

    Equivalent to the following:
        ```
        my $plate = $self->schema->resultset('FlgenPlate')->search
            ({plate_barcode => $fluidigm_barcode,
            well_label    => $well_address},
            {prefetch      => ['sample', 'study']});
        ```
    """

    result = sess.query(FlgenPlate).filter(
        (FlgenPlate.plate_barcode == plate_barcode)
        & (FlgenPlate.well_label == well_label)
    )

    return result
