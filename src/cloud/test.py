from abc import ABC, abstractmethod
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import socket

# CloudClient
AZURITE_URL = os.getenv("AZURITE_URL")
AZURITE_ACCOUNT_NAME = os.getenv("AZURITE_ACCOUNT_NAME")
AZURITE_ACCOUNT_KEY = os.getenv("AZURITE_ACCOUNT_KEY")
PAPER_CONTAINER_NAME = os.getenv("PAPER_CONTAINER_NAME")
CONNECTION_STRING = f"DefaultEndpointsProtocol=http;AccountName={AZURITE_ACCOUNT_NAME};AccountKey={AZURITE_ACCOUNT_KEY};BlobEndpoint={AZURITE_URL};"

if __name__ == "__main__":
    client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = client.get_blob_client(container=PAPER_CONTAINER_NAME, blob="raw/sample.pdf")
    with open("do1.pdf", "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
