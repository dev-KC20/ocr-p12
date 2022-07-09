""" create a test DB by copy of the actual one




[(c)](https://pytest-django.readthedocs.io/en/latest/database.html?highlight=create%20database#using-a-template-database-for-tests) 

"""

import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database="postgres", user="postgres", password="oc-password1")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    settings.DATABASES["default"]["NAME"] = "test_eecrm"

    run_sql("DROP DATABASE IF EXISTS test_eecrm")
    run_sql("CREATE DATABASE test_eecrm TEMPLATE eecrm")

    yield

    for connection in connections.all():
        connection.close()

    run_sql("DROP DATABASE test_eecrm")
