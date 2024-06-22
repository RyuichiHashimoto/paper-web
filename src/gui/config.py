import os


class Config:
    DATABASE = {
        "name": "example.db",
        "engine": "peewee.MysqlDatabase",
    }
    # SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"  # SQLiteの場合
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
