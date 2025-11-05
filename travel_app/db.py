import psycopg2
import os
from flask import g
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extensions import connection as Psycopg2Connection

pool = ThreadedConnectionPool(minconn=1, maxconn=5, dsn=os.environ["DATABASE_URL"])


def get_db() -> Psycopg2Connection:
    if "db_conn" not in g:
        g.db_conn = pool.getconn()
    return g.db_conn


def release_conn(error=None) -> None:
    conn = g.pop("db_conn", None)
    if conn is not None:
        pool.putconn(conn)
