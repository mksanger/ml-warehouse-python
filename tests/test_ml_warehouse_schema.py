from pytest import mark as m

from tests.ml_warehouse_fixture import mlwh_session

# Stop IDEs "optimizing" away this import
_ = mlwh_session
