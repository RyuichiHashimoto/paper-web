from peewee import MySQLDatabase
from contextlib import contextmanager
from typing import Generator

parameter = {
    "database": "paper-db",  # データベース名
    "user": "hashimoto",  # ユーザー名
    "password": "hashimoto",  # パスワード
    "host": "paper-db",  # ホスト名
    "port": 3306,  # ポート番号
}
DB = MySQLDatabase(**parameter)
DB.connect()
