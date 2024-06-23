from peewee import Model, CharField, DateField, BooleanField, MySQLDatabase, CompositeKey, ForeignKeyField, TextField, DoesNotExist
from db.db import DB
from datetime import date


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
    cloudfilepath = TextField(null=True)


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


def get_cloudfilepath_from_paper_id(paper_id: str) -> str | None:
    try:
        ret = Paper_WebMetaInfo.get(Paper_WebMetaInfo.paper_id == paper_id)
        return getattr(ret, "cloudfilepath")
    except DoesNotExist:
        return None


def increment_paper_id(paper_id: str) -> str:
    """paper_idをインクリメントする。"""
    value = int(paper_id.split("-")[1]) + 1
    if value >= 100000:
        raise ValueError("paper_id is too large.")

    return f"P-{value:05d}"


def get_new_paper_id() -> str:
    """次のpaper_idを取得する。"""
    return increment_paper_id(fetch_max_id_from_papertable())


def fetch_max_id_from_papertable() -> str | None:
    """paper_idの最大値を取得する。なければ、DoesNotExistを返す。"""
    return Paper.select().order_by(Paper.paper_id.desc()).get().paper_id


def insert_paper_record_to_db(
    title: str, pdf_cloud_file_path: str, description: str = "", source_reference: str = "", url: str = "", public_date: date | None = None
) -> None:
    """新しい論文をDBに追加する。

    parameter
    ---------
        title: str 論文のタイトル
        pdf_cloud_file_path: str  論文のPDFファイルのパス
        description: str  論文の説明
        source_reference: str  論文の引用元
        url: str  論文のURL
        public_date: date  論文の公開日

    return
    ------
        None
    """
    new_paper_id = get_new_paper_id()
    created_at = date.today()
    last_modified = date.today()

    Paper.create(
        paper_id=new_paper_id,
        title=title,
        abstract="",
        description=description,
        source_reference=source_reference,
        url=url,
        public_date=public_date,
        created_at=created_at,
        last_modified=last_modified,
    )
    Paper_WebMetaInfo.create(paper_id=new_paper_id, cloudfilepath=pdf_cloud_file_path)


def update_paper_record(paper_id: str, title: str, description: str, source_reference: str, url: str, public_date: date) -> bool:
    """論文情報を更新する。

    parameter
    ---------
        paper_id: str 論文ID
        title: str 論文のタイトル
        description: str  論文の説明
        source_reference: str  論文の引用元
        url: str  論文のURL
        public_date: date  論文の公開日

    return
    ------
        None
    """
    paper = Paper.get(Paper.paper_id == paper_id)

    if paper is None:
        return False

    paper.title = title
    paper.description = description
    paper.source_reference = source_reference
    paper.url = url
    paper.public_date = public_date
    paper.last_modified = date.today()
    paper.save()
    return True


if __name__ == "__main__":
    DB.create_tables([Paper, Category, PaperCategory, Author, PaperAuthor, Chapter])
