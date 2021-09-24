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
