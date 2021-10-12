from setuptools import setup

setup(
    name="ml-warehouse",
    version="0.1.0",
    packages=["ml_warehouse"],
    url="https://github.com/absanger/ml-warehouse-python",
    license="GPL3",
    author="Adam Blanchet",
    author_email="ab59@sanger.ac.uk",
    description="Python SQLAlchemy bindings to a warehouse housing data from multiple LIM systems.",
    install_requires=[
        "sqlalchemy>=1.4",
        "sqlalchemy-utils >=0.37.8,<0.38",
        "cryptography >=3.4.8,<3.5",
        "pymysql >=1.0.2,<1.1",
    ],
    tests_require=["pytest>=6.2.2", "pytest-it==0.1.4", "pyyaml==5.4.1"],
)
