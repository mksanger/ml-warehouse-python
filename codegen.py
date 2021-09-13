import os
import subprocess

PW = os.environ["MYSQL_PW"]
USER = os.environ["MYSQL_USER"]
HOST = os.environ["MYSQL_HOST"]
PORT = os.environ["MYSQL_PORT"]
DBNAME = os.environ["MYSQL_DBNAME"]

url = "mysql+pymysql://{user}:{passw}@{host}:{port}/{db}?charset=utf8mb4".format(
    user=USER, passw=PW, host=HOST, port=PORT, db=DBNAME
)

# Generate the declarative mappings.
subprocess.run(
    [
        "sqlacodegen",
        url,
        "--outfile",
        "generated.py",
    ]
)

# Workaround issue with CHAR.
subprocess.run(
    ["sed", "-i.bu", "/sqlalchemy.dialects.mysql/s/CHAR, *//", "generated.py"]
)
os.remove("generated.py.bu")

# Move the generated file.
os.rename("generated.py", "ml_warehouse/ml_warehouse_schema.py")
