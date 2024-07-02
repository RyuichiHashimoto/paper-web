import os
import pdf2image
import layoutparser as lp
import base64
import numpy as np
import cv2
from io import BytesIO


FILEBYTES = str


def pdf_to_base64(pdf_path: str) -> list[FILEBYTES]:
    """
    PDFをbase64エンコードされた画像のリストに変換する。

    Args:
        pdf_path (str): 変換するPDFファイルのパス

    Returns:
        list: base64エンコードされた画像のリスト
    """
    images = pdf2image.convert_from_path(pdf_path)

    base64_images = []

    for image in images:
        buffered = BytesIO()
        image.save(buffered, format="jpeg")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        base64_images.append(img_str)

    return base64_images


if __name__ == "__main__":
    extract_figures_and_tables("cec664dd-e778-4cb3-92b6-0ac1ecafb9f5.pdf", "./to")
