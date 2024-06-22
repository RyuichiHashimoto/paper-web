from db.model import Paper, Category, PaperCategory, Auther, PaperAuther, Chapter
from datetime import date

if __name__ == "__main__":
    # DB.connect()

    table_list = [PaperCategory, PaperAuther, Chapter, Paper, Auther, Category]
    for table in table_list:
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

    auther_list = [
        {
            "auther_id": "A-00001",
            "name": "Ryuichi Hashimoto",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "auther_id": "A-00002",
            "name": "Hisao Ishibuchi",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "auther_id": "A-00003",
            "name": "Naoki Masuyama",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "auther_id": "A-00004",
            "name": "Yusuke Nojima",
            "affiliation": "Osaka Prefecture University",
        },
        {
            "auther_id": "A-00005",
            "name": "Toshiki Urita",
            "affiliation": "Osaka Prefecture University",
        },
    ]
    paper_auther_list = [
        {"paper_id": "P-00001", "auther_id": "A-00001"},
        {"paper_id": "P-00001", "auther_id": "A-00002"},
        {"paper_id": "P-00001", "auther_id": "A-00003"},
        {"paper_id": "P-00001", "auther_id": "A-00004"},
        {"paper_id": "P-00002", "auther_id": "A-00001"},
        {"paper_id": "P-00002", "auther_id": "A-00002"},
        {"paper_id": "P-00002", "auther_id": "A-00003"},
        {"paper_id": "P-00002", "auther_id": "A-00004"},
        {"paper_id": "P-00002", "auther_id": "A-00005"},
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

    Paper.insert_many(paper_list).execute()
    Auther.insert_many(auther_list).execute()
    PaperAuther.insert_many(paper_auther_list).execute()
    Category.insert_many(category_list).execute()
    PaperCategory.insert_many(paper_category_list).execute()
