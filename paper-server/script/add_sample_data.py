from db.db import DB
from db.model import Paper, Category, PaperCategory, Auther, PaperAuther, Chapter

if __name__ == "__main__":
    # DB.connect()

    table_list = [PaperCategory, PaperAuther, Chapter, Paper, Auther, Category]
    for table in table_list:
        table.drop_table()

    for table in table_list[::-1]:
        table.create_table()
