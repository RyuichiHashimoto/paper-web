from db.model import Paper, Category, PaperCategory, Author, PaperAuthor, Chapter, Paper_WebMetaInfo, Paper_LLMSummary, LLMPrompt
from datetime import date
from llmlib.summalizer import PROMPT

if __name__ == "__main__":
    # DB.connect()

    table_list = [LLMPrompt]
    for table in table_list:
        print(table.__name__)
        table.drop_table()

    for table in table_list[::-1]:
        table.create_table()

    LLM_PROMPT = [
        {
            "prompt_id": "L-00001",
            "prompt": PROMPT,
        }
    ]

    LLMPrompt.insert_many(LLM_PROMPT).execute()

    print("Finish")
