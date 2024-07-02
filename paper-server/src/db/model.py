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
    title = TextField(null=True)
    abstract = TextField(null=True)
    description = TextField(null=True)
    source_reference = TextField(null=True)
    url = TextField(null=True)
    public_date = DateField(null=True)
    created_at = DateField(null=False)
    last_modified = DateField(null=False)

    # def save(self, *args, **kwargs):
    #     return super(Paper, self).save(*args, **kwargs)

    #     with self._meta.database.atomic() as transaction:
    #         try:
    #             result = super(Paper, self).save(*args, **kwargs)
    #             if result == 0:
    #                 raise Exception("Failed to save Paper record.")

    #             same_cretae_table_list = [Paper_LLMSummary, Paper_WebMetaInfo]
    #             for table in same_cretae_table_list:
    #                 if not table.get_or_none(table.paper_id == self.paper_id):
    #                     table.create(paper_id=self.paper_id)

    #             return result

    #         except Exception as e:
    #             transaction.rollback()
    #             # print(e)
    #             raise e


class LLMPrompt(BaseModel):
    prompt_id = CharField(primary_key=True, max_length=255)
    name = TextField()
    prompt = TextField()


class Paper_LLMSummary(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="summary", on_delete="CASCADE")
    prompt_id = ForeignKeyField(LLMPrompt, backref="summary", on_delete="CASCADE")
    summary = TextField(default="")

    class Meta:
        primary_key = CompositeKey("paper_id", "prompt_id")


class Paper_WebMetaInfo(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="metainfo", on_delete="CASCADE")
    visible = BooleanField(default=True)
    cloudfilepath = TextField(default="")


class Category(BaseModel):
    category_id = CharField(primary_key=True, max_length=255)
    category = CharField()


class PaperCategory(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="categories", on_delete="CASCADE")
    category_id = ForeignKeyField(Category, backref="papers", on_delete="CASCADE")

    class Meta:
        primary_key = CompositeKey("paper_id", "category_id")


class Author(BaseModel):
    author_id = CharField(primary_key=True, max_length=255)
    name = CharField()
    affiliation = CharField(null=True)


class PaperAuthor(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="authors", on_delete="CASCADE")
    author_id = ForeignKeyField(Author, backref="papers", on_delete="CASCADE")

    class Meta:
        primary_key = CompositeKey("paper_id", "author_id")


class Chapter(BaseModel):
    paper_id = ForeignKeyField(Paper, backref="chapters", on_delete="CASCADE")
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


def __incremental_id(id: str, prefix: str) -> str:
    """IDをインクリメントする。"""
    if prefix == "":
        raise ValueError("prefix is empty.")

    value = int(id.split("-")[1]) + 1
    if value >= 100000:
        raise ValueError("id is too large.")

    return f"{prefix}-{value:05d}"


## Paper Table


def increment_paper_id(paper_id: str) -> str:
    return __incremental_id(paper_id, "P")


def get_new_paper_id() -> str:
    """次のpaper_idを取得する。"""
    return increment_paper_id(fetch_max_id_from_papertable())


def fetch_max_id_from_papertable() -> str | None:
    """paper_idの最大値を取得する。なければ、DoesNotExistを返す。"""
    return Paper.select().order_by(Paper.paper_id.desc()).get().paper_id


## LLM Table
def increment_llmprompt_id(prompt_id: str) -> str:
    return __incremental_id(prompt_id, "L")


def get_new_llmprompt_id() -> str:
    """次のllmprompt_idを取得する。"""
    return increment_llmprompt_id(fetch_max_id_from_papertable())


def fetch_max_id_from_papertable() -> str | None:
    """llmprompt_idの最大値を取得する。なければ、DoesNotExistを返す。"""
    return LLMPrompt.select().order_by(LLMPrompt.prompt_id.desc()).get().prompt_id


## Paper_LLMSummary Table
def update_llmsummary_record_to_db(paper_id: str, prompt_id: str, summaryresult: str) -> None:
    """論文をLLMで要約した内容をDBに追加する。

    parameter
    ---------
        paper_id: str 論文ID
        prompt_id: str  prompt ID
        summaryresult: str  LLMの結果

    return
    ------
        None
    """
    if Paper_LLMSummary.get_or_none(paper_id=paper_id, prompt_id=prompt_id):
        Paper_LLMSummary.update(summary=summaryresult).where(Paper_LLMSummary.paper_id == paper_id, Paper_LLMSummary.prompt_id == prompt_id).execute()
    else:
        Paper_LLMSummary.create(paper_id=paper_id, prompt_id=prompt_id, summary=summaryresult)


def get_llm_summary_from_db(paper_id: str, prompt_id: str) -> str | None:
    """指定した論文IDとprompt_idの組み合わせのレコードを取得する。

    parameter
    ---------
        paper_id: str 論文ID
        prompt_id: str  prompt ID

    return
    ------
        str
    """
    try:
        return Paper_LLMSummary.get(Paper_LLMSummary.paper_id == paper_id, Paper_LLMSummary.prompt_id == prompt_id).summary
    except DoesNotExist:
        return None


def exist_llmsummary_record(paper_id: str, prompt_id: str) -> bool:
    """指定した論文IDとprompt_idの組み合わせのレコードが存在するか確認する。

    parameter
    ---------
        paper_id: str 論文ID
        prompt_id: str  prompt ID

    return
    ------
        bool
    """
    return Paper_LLMSummary.get_or_none(paper_id=paper_id, prompt_id=prompt_id) is not None


def fetch_max_id_from_papertable() -> str | None:
    """paper_idの最大値を取得する。なければ、DoesNotExistを返す。"""
    return Paper.select().order_by(Paper.paper_id.desc()).get().paper_id


def insert_paper_record_to_db(
    title: str, pdf_cloud_file_path: str, abstract: str = "", source_reference: str = "", url: str = "", public_date: date | None = None
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
        abstract=abstract,
        source_reference=source_reference,
        url=url,
        public_date=public_date,
        created_at=created_at,
        last_modified=last_modified,
    )
    Paper_WebMetaInfo.create(paper_id=new_paper_id, cloudfilepath=pdf_cloud_file_path)
    Paper_LLMSummary.create(paper_id=new_paper_id)


def update_paper_record(paper_id: str, title: str, abstract: str, source_reference: str, url: str, public_date: date) -> bool:
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
    paper.abstract = abstract
    paper.source_reference = source_reference
    paper.url = url
    paper.public_date = public_date
    paper.last_modified = date.today()
    paper.save()
    return True


def get_paper_list_as_list() -> list[dict[str, any]]:
    papers = Paper.select(Paper.paper_id, Paper.title, Paper.last_modified)
    return [{"id": paper.paper_id, "title": paper.title, "last_modified": paper.last_modified} for paper in papers]


def get_llmprompt_list_as_list() -> list[dict[str, any]]:
    prompts = LLMPrompt.select(LLMPrompt.prompt_id, LLMPrompt.name, LLMPrompt.prompt)
    return [{"id": prompt.prompt_id, "name": prompt.name, "prompt": prompt.prompt} for prompt in prompts]


def get_llmprompt_id_name_list() -> list[dict[str, any]]:
    prompts = LLMPrompt.select(LLMPrompt.prompt_id, LLMPrompt.name)
    return [{"id": prompt.prompt_id, "name": prompt.name} for prompt in prompts]


def get_paper_metainfo_from_db(paper_id: str) -> dict[str, any] | None:

    try:
        paper = Paper.get(Paper.paper_id == paper_id)
        authors = Author.select().join(PaperAuthor, on=(Author.author_id == PaperAuthor.author_id)).where(PaperAuthor.paper_id == paper_id)
        author_list = [author.name for author in authors]

        return {
            "id": paper.paper_id,
            "authors": ", ".join(author_list),
            "title": paper.title,
            "abstract": paper.abstract,
            "source_reference": paper.source_reference,
            "url": paper.url,
            "public_date": paper.public_date,
        }

    except DoesNotExist:
        return None


def insert_llmsummary_record_to_db(paper_id: str, prompt_id: str, summary: str, exist_ok=True) -> bool:
    """論文をLLMで要約した内容をDBに追加する。

    parameter
    ---------
        paper_id: str 論文ID
        prompt_id: str  prompt ID
        summary: str  LLMの結果
        exist_ok: bool  既存レコードが存在する場合、更新を許可するかどうか

    return
    ------
        True: 既存レコードの更新もしくは、新規レコードの追加
        False: 既存レコードが存在し、かつexist_okがFalseの場合、何もしない。
    """
    exist_flag = exist_llmsummary_record(paper_id, prompt_id)

    if exist_flag and not exist_ok:
        return False  # レコードが存在するが、更新を許可しない場合、何もしない。

    if exist_flag:
        Paper_LLMSummary.update(summary=summary).where(Paper_LLMSummary.paper_id == paper_id, Paper_LLMSummary.prompt_id == prompt_id).execute()
    else:
        Paper_LLMSummary.create(paper_id=paper_id, prompt_id=prompt_id, summary=summary)

    return True


if __name__ == "__main__":
    print(get_paper_metainfo_from_db("P-0000"))
    # update_paper_record(
    #     paper_id="P-00004",
    #     title="Sample",
    #     abstract="This paper discusses innovative approaches to machine learning.",
    #     source_reference="Proceedings of the genetic and evolutionary computation conference companion",
    #     url="https://dl.acm.org/doi/abs/10.1145/3205651.3208228",
    #     public_date=date(2018, 7, 6),
    # )

    # DB.create_tables([Paper, Category, PaperCategory, Author, PaperAuthor, Chapter])
