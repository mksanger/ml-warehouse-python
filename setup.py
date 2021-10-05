from setuptools import setup

setup(
    name="ml_warehouse",
    version="0.1.0",
    packages=["ml_warehouse"],
    url="https://github.com/absanger/ml-warehouse-python",
    license="GPL3",
    author="Adam Blanchet",
    author_email="ab59@sanger.ac.uk",
    description="Automation for processing DNA sequence data",
    install_requires=[
        "sqlalchemy>=1.4",
    ],
    tests_require=["pytest", "pytest-it"],
)
