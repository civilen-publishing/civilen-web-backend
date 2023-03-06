import os

from fastapi import UploadFile


def saveFile(file: UploadFile, path: str, filename: str) -> str:
    """
    Save a file to a given path with a given filename

    Args:
        file (UploadFile): The file to save
        path (str): The path to save the file to
        filename (str): The filename to save the file as

    Returns:
        str: The path to the saved file
    """
    if file is None:
        return ""

    fullPath = f"{path}/{filename}.{file.filename.split('.')[-1]}"
    with open(fullPath, "wb") as buffer:
        buffer.write(file.file.read())
    return fullPath


def validateImage(file: UploadFile) -> bool:
    """
    Validate an image file

    Args:
        file (UploadFile): The file to validate

    Returns:
        bool: True if the file is a valid image, False otherwise
    """
    if file is None:
        return False
    return file.content_type in ["image/png", "image/jpeg", "image/jpg"]


def removeFile(path: str) -> bool:
    """
    Remove a file from a given path

    Args:
        path (str): The path to the file to remove

    Returns:
        bool: True if the file was removed, False otherwise
    """
    if path == "":
        return False
    if os.path.exists(path):
        os.remove(path)
        return True
    return False