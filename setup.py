from setuptools import setup

setup(
    name="ml-warehouse",
    version="0.1.0",
    packages=["ml_warehouse"],
    url="https://github.com/absanger/ml-warehouse-python",
    license="GPL3",
    author="Adam Blanchet",
    author_email="ab59@sanger.ac.uk",
    description="Python SQLAlchemy bindings to a warehouse housing data "
    "from multiple LIM systems.",
    install_requires=[
        "sqlalchemy >= 1.4",
        "sqlalchemy-utils",
        "cryptography",
        "pymysql",
    ],
    tests_require=["black", "pytest", "pytest-it", "pyyaml"],
)
