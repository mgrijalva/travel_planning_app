from psycopg2.extensions import connection as Psycopg2Connection
from dataclasses import dataclass
from typing import List


def dummy_function(a: int, b: int) -> int:
    """Just for testing pytest"""
    return a + b


@dataclass(frozen=True)
class Trip:
    id: int
    name: str


class TripsRepository:
    def __init__(self, conn: Psycopg2Connection):
        self.conn = conn

    def all(self) -> List[Trip]:
        with self.conn.cursor() as cursor:
            cursor.execute("select 1,2,3")
            for row in cursor.fetchall():
                print(row)

            return [Trip(1, "test"), Trip(2, "test data")]
