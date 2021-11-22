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

from setuptools import find_packages, setup

setup(
    name="ml-warehouse",
    url="https://github.com/absanger/ml-warehouse-python",
    license="GPL3",
    author="Adam Blanchet",
    author_email="ab59@sanger.ac.uk",
    description="Python SQLAlchemy bindings to a warehouse housing data "
    "from multiple LIM systems.",
    use_scm_version=True,
    python_requires=">=3.8",
    packages=find_packages("src"),
    package_dir={"": "src"},
    setup_requires=["setuptools_scm"],
    install_requires=[
        "sqlalchemy >= 1.4",
        "sqlalchemy-utils",
        "cryptography",
        "pymysql",
    ],
    tests_require=["black", "pytest", "pytest-it", "pyyaml"],
)
