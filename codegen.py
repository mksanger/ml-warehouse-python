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

# Move the generated file.
os.rename("generated.py", "ml_warehouse/ml_warehouse_schema.py")

# Decorate the classes
result = []
decorator_added = False
with open("ml_warehouse/ml_warehouse_schema.py", "r") as read_file:

    result.append("from ml_warehouse._decorators import add_docstring\n")

    for line in read_file.readlines():

        if line.startswith("class"):
            result.append("@add_docstring\n")

        result.append(line)

with open("ml_warehouse/ml_warehouse_schema.py", "w") as write_file:
    write_file.writelines(result)
