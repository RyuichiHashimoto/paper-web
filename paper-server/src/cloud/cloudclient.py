from abc import ABC, abstractmethod
import os

# CloudClient
AZURITE_URL = os.getenv("AZURITE_URL")
AZURITE_ACCOUNT_NAME = os.getenv("AZURITE_ACCOUNT_NAME")
AZURITE_ACCOUNT_KEY = os.getenv("AZURITE_ACCOUNT_KEY")
PAPER_CONTAINER_NAME = os.getenv("PAPER_CONTAINER_NAME")
CONNECTION_STRING = f"DefaultEndpointsProtocol=http;AccountName={AZURITE_ACCOUNT_NAME};AccountKey={AZURITE_ACCOUNT_KEY};BlobEndpoint={AZURITE_URL};"


class CloudClient(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def donwload(self, cloud_file_path: str, local_file_path) -> str:
        pass

    @abstractmethod
    def upload(self, path: str):
        pass

    @abstractmethod
    def exist_file(self, path: str) -> bool:
        pass

    # @abstractmethod
    # def send_queue_message(self, path: str):
    #     pass

    # @abstractmethod
    # def pop_queue_message(self, path: str):
    #     pass


if __name__ == "__main__":
    client = AzuriteCloudClient()
    client.donwload("raw/sample.pdf", "./sample.pdf")
