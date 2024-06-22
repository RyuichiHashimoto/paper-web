import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"  # SQLiteの場合
    SQLALCHEMY_TRACK_MODIFICATIONS = False
