const { BlobServiceClient } = require('@azure/storage-blob');
const { AbortController } = require('@azure/abort-controller');
const fs = require('fs');

async function main() {
    // Azariteのデフォルト接続文字列
    const AZURE_STORAGE_CONNECTION_STRING = "UseDevelopmentStorage=true";

    // BlobServiceClientを作成
    const blobServiceClient = BlobServiceClient.fromConnectionString(AZURE_STORAGE_CONNECTION_STRING);

    // 新しいコンテナの名前
    const containerName = 'mycontainer';
    const containerClient = blobServiceClient.getContainerClient(containerName);

    // コンテナを作成（既に存在する場合は無視されます）
    await containerClient.createIfNotExists();

    // 作成するBlobの名前
    const blobName = 'myblob.txt';
    const blockBlobClient = containerClient.getBlockBlobClient(blobName);

    // アップロードするファイルの内容
    const content = 'Hello, Azurite!';
    const uploadBlobResponse = await blockBlobClient.upload(content, Buffer.byteLength(content));

    console.log(`Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`);
}

main().catch((err) => {
    console.error("Error running sample:", err.message);
});
