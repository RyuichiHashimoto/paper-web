from peewee import Model, CharField, DateField, BooleanField, MySQLDatabase, PrimaryKeyField, IntegerField, CompositeKey, ForeignKeyField, TextField
from db.db import DB


# 基本モデルクラス
class BaseModel(Model):
    class Meta:
        database = DB

    @classmethod
    def set_database(cls, database: MySQLDatabase) -> None:
        cls._meta.database = database


class Paper(BaseModel):
    paper_id = CharField(primary_key=True, max_length=255)
    title = TextField()
    abstract = TextField(null=True)
    description = TextField(null=True)
    source_reference = TextField(null=True)
    url = TextField(null=True)
    public_date = DateField(null=True)
    created_at = DateField()
    last_modified = DateField()


class Paper_WebMetaInfo(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="metainfo")
    visible = BooleanField(default=True)


class Category(BaseModel):
    category_id = CharField(primary_key=True, max_length=255)
    category = CharField()


class PaperCategory(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="categories")
    category_id = ForeignKeyField(Category, backref="papers")

    class Meta:
        primary_key = CompositeKey("paper_id", "category_id")


class Author(BaseModel):
    author_id = CharField(primary_key=True, max_length=255)
    name = CharField()
    affiliation = CharField(null=True)


class PaperAuthor(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="authors")
    author_id = ForeignKeyField(Author, backref="papers")

    class Meta:
        primary_key = CompositeKey("paper_id", "author_id")


class Chapter(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="chapters")
    chapter_id = CharField()
    title = CharField()
    content = CharField(null=True)
    summary = CharField(null=True)

    class Meta:
        primary_key = CompositeKey("paper_id", "chapter_id")


if __name__ == "__main__":
    DB.create_tables([Paper, Category, PaperCategory, Author, PaperAuthor, Chapter])
