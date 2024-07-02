from db.model import Paper, Category, PaperCategory, Author, PaperAuthor, Chapter, Paper_WebMetaInfo, Paper_LLMSummary, LLMPrompt
from datetime import date
from llmlib.summalizer import PROMPT

if __name__ == "__main__":
    # DB.connect()

    table_list = [
        Paper_LLMSummary,
        Paper_WebMetaInfo,
        PaperCategory,
        PaperAuthor,
        Chapter,
        Author,
        Category,
        LLMPrompt,
        Paper,
    ]
    for table in table_list:
        print(table.__name__)
        table.drop_table()

    for table in table_list[::-1]:
        table.create_table()

    paper_list = [
        {
            "paper_id": "P-00001",
            "title": "Analysis of evolutionary multi-tasking as an island model",
            "abstract": "This paper discusses innovative approaches to machine learning.",
            "description": "",
            "source_reference": "Proceedings of the genetic and evolutionary computation conference companion",
            "url": "https://dl.acm.org/doi/abs/10.1145/3205651.3208228",
            "public_date": date(2018, 7, 6),
            "created_at": date(2024, 6, 22),
            "last_modified": date(2024, 6, 22),
        },
        {
            "paper_id": "P-00002",
            "title": "Effects of local mating in inter-task crossover on the performance of decomposition-based evolutionary multiobjective multitask optimization algorithms",
            "abstract": "This paper discusses innovative approaches to machine learning.",
            "description": "",
            "source_reference": "2020 IEEE Congress on Evolutionary Computation (CEC)",
            "url": "https://ieeexplore.ieee.org/abstract/document/9185871/",
            "public_date": date(2020, 7, 19),
            "created_at": date(2024, 6, 22),
            "last_modified": date(2024, 6, 22),
        },
    ]

    author_list = [
        {
            "author_id": "A-00001",
            "name": "Ryuichi Hashimoto",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "author_id": "A-00002",
            "name": "Hisao Ishibuchi",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "author_id": "A-00003",
            "name": "Naoki Masuyama",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "author_id": "A-00004",
            "name": "Yusuke Nojima",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "author_id": "A-00005",
            "name": "Toshiki Urita",
            "affiliation": "Osaka Prefecture University",
        },
    ]
    paper_author_list = [
        {"paper_id": "P-00001", "author_id": "A-00001"},
        {"paper_id": "P-00001", "author_id": "A-00002"},
        {"paper_id": "P-00001", "author_id": "A-00003"},
        {"paper_id": "P-00001", "author_id": "A-00004"},
        {"paper_id": "P-00002", "author_id": "A-00001"},
        {"paper_id": "P-00002", "author_id": "A-00002"},
        {"paper_id": "P-00002", "author_id": "A-00003"},
        {"paper_id": "P-00002", "author_id": "A-00004"},
        {"paper_id": "P-00002", "author_id": "A-00005"},
    ]
    category_list = [
        {"category_id": "C-00001", "category": "multi-tasking"},
        {"category_id": "C-00002", "category": "island model"},
        {"category_id": "C-00003", "category": "multi-objective optimization"},
    ]
    paper_category_list = [
        {"paper_id": "P-00001", "category_id": "C-00001"},
        {"paper_id": "P-00001", "category_id": "C-00002"},
        {"paper_id": "P-00002", "category_id": "C-00001"},
        {"paper_id": "P-00002", "category_id": "C-00003"},
    ]
    paper_metadata_list = [
        {
            "paper_id": "P-00001",
            "cloudfilepath": f"raw/cec664dd-e778-4cb3-92b6-0ac1ecafb9f5.pdf",
        },
        {
            "paper_id": "P-00002",
            "cloudfilepath": f"raw/0b50b30c-ec6a-41f8-b67f-3cba90330362.pdf",
        },
    ]
    LLM_PROMPT = [
        {
            "prompt_id": "L-00001",
            "prompt": PROMPT,
        }
    ]

    Paper.insert_many(paper_list).execute()
    Author.insert_many(author_list).execute()
    PaperAuthor.insert_many(paper_author_list).execute()
    Category.insert_many(category_list).execute()
    PaperCategory.insert_many(paper_category_list).execute()
    Paper_WebMetaInfo.insert_many(paper_metadata_list).execute()
    LLMPrompt.insert_many(LLM_PROMPT).execute()

    print("Finish")
