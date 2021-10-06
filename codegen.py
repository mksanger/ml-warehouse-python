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
