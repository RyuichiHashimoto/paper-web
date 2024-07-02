from abc import ABC, abstractmethod
from openai import OpenAI


OPENAI_CLIENT = OpenAI()


class model(ABC):
    @abstractmethod
    def name():
        pass


class GPT3_5(model):
    @property
    def name(self):
        return "gpt-3.5-turbo"

    def __init__(self):
        self.model = self.name

    def chat(self, messages: str):
        completion = OPENAI_CLIENT.chat.completions.create(model=self.model, messages=messages)
        return completion.choices[0].message


class GPT4o(model):
    @property
    def name(self):
        return "gpt-4o"

    def __init__(self):
        self.model = self.name

    def chat(self, messages: str):
        completion = OPENAI_CLIENT.chat.completions.create(model=self.model, messages=messages)
        return completion.choices[0].message


if __name__ == "__main__":
    client = GPT3_5()

    messages = [
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."},
    ]
    print(client.chat(messages))
