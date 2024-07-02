import os
from pdf.extract import pdf_to_base64
from llmlib.model import GPT4o


PROMPT = """
### who are you?
    you are a great researcher. 
    
### Summarize Research Paper
    - **paper-title**: [Title of the paper]
    - **Objective**: Please summarize the research paper I provide, focusing on the main points and findings. Your summary should be concise, objective, and accurately represent the content of the paper. Please avoid personal opinions or interpretations and present the information in your own words.
    
### Summary
    - **Main Points**: [Provide a brief summary of the main points]
    - **Findings**: [Outline the key findings of the research]    

### Analysis
    - **Repeated Words**: [List the most repeated words in the paper]
    - **General Idea**: [Describe the general idea of the paper]
    - **Problem**: [Identify the problem that the study is addressing]
    - **Proposed Solution**: [Explain the proposed solution to the problem]
"""


def summarize_paper_summary_via_image(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    images = pdf_to_base64(file_path)
    messages = [
        {"role": "system", "content": PROMPT},
        {
            "role": "user",
            "content": [
                *map(
                    lambda x: {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpg;base64,{x}",
                            "detail": "low",
                        },
                    },
                    images,
                )
            ],
        },
    ]
    return GPT4o().chat(messages)
