from cloud.cloudclient import CloudClient
from azure.storage.blob import BlobServiceClient
import os
import uuid

# CloudClient
AZURITE_URL = os.getenv("AZURITE_URL")
AZURITE_ACCOUNT_NAME = os.getenv("AZURITE_ACCOUNT_NAME")
AZURITE_ACCOUNT_KEY = os.getenv("AZURITE_ACCOUNT_KEY")
PAPER_CONTAINER_NAME = os.getenv("PAPER_CONTAINER_NAME")
CONNECTION_STRING = f"DefaultEndpointsProtocol=http;AccountName={AZURITE_ACCOUNT_NAME};AccountKey={AZURITE_ACCOUNT_KEY};BlobEndpoint={AZURITE_URL};"


class AzuriteStorageClient(CloudClient):

    def __init__(self):
        super().__init__()
        self.client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        self.container_client = self.client.get_container_client(PAPER_CONTAINER_NAME)

    def donwload(self, cloud_file_path: str, local_file_path: str):
        blob_client = self.container_client.get_blob_client(cloud_file_path)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        with open(local_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def upload(self, local_file_path: str, cloud_file_path: str):
        blob_client = self.container_client.get_blob_client(cloud_file_path)

        with open(local_file_path, "rb") as upload_file:
            blob_client.upload_blob(upload_file)

    def exist_file(self, cloud_file_path: str) -> bool:
        blob_client = self.container_client.get_blob_client(cloud_file_path)
        return blob_client.exists()


def generate_unique_paper_uuid() -> str:
    """ユニークな論文管理用UUIDを返す。"""
    # return "P-" + str(int(fetch_max_id_from_papertable().split("-")[1]) + 1).zfill(5)
    client = AzuriteStorageClient()

    uuidvalue = uuid.uuid4()
    while client.exist_file(f"raw/{uuidvalue}.pdf"):
        uuidvalue = uuid.uuid4()
    return uuidvalue


if __name__ == "__main__":
    client = AzuriteStorageClient()
    client.donwload("raw/sample.pdf", "./sample.pdf")
    client.upload("./sample.pdf", "raw/sample111.pdf")
