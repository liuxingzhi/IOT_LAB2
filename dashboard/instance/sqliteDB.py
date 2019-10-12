# coding=utf8
from __future__ import annotations
from typing import Dict, List, Optional, Union, Tuple, TypeVar, Sequence
import sqlite3
from DBUtils.PooledDB import PooledDB, PooledDedicatedDBConnection, PooledSharedDBConnection
from tabulate import tabulate
import pandas as pd
from collections import OrderedDict
import logging

logging.basicConfig(level=logging.INFO)


class SqliteDB:
    __pool = None

    def __init__(self, db_name: str = "data.sqlite") -> None:
        self._connection = SqliteDB.get_conn(db_name)
        self.cursor = self._connection.cursor()

    @staticmethod
    def get_conn(db_name: str = "school.sqlite3") -> Union[PooledSharedDBConnection, PooledDedicatedDBConnection]:
        """
        静态方法，从连接池中取出连接
        return sqlite.connection
        """
        if SqliteDB.__pool is None:
            SqliteDB.__pool = PooledDB(creator=sqlite3, mincached=1, maxcached=5, database=db_name)
        return SqliteDB.__pool.connection()

    def executescript(self, commands: str):
        self.cursor.executescript(commands)

    def execute_from_file(self, filename: str):
        with open(filename, "r") as f:
            commands = f.read()
            self.cursor.executescript(commands)

    def fetchall(self) -> List[Tuple]:
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def __enter__(self) -> SqliteDB:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


def test_query_title():
    db = SqliteDB()
    sql = "select id from kafkatest1 where id =: id"
    result = db.query_title(sql, {'id': 1000})
    for r in result:
        print(r)


if __name__ == '__main__':
    # test_query_title()
    db = SqliteDB()
    db2 = SqliteDB()
    # # db.backup(table)
    # db.copy_table(table2, table)
    # db.backup(table)
    # sql = "select * from ? where sender = ?"
    # temp = db.query_by(sql,['msgapp_msgboard', 'kafka'])
    # print(temp)
