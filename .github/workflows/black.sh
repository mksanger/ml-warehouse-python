#!/bin/sh

pip3 install black
black --check --diff --color . --force-exclude ml_warehouse/ml_warehouse_schema.py