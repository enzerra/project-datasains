from pathlib import Path

from fastapi import UploadFile

from app.config import settings


async def save_upload_file(upload_file: UploadFile, destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with destination.open("wb") as buffer:
        while chunk := await upload_file.read(1024 * 1024):
            size += len(chunk)
            buffer.write(chunk)
    await upload_file.close()
    return size


def validate_extension(filename: str) -> None:
    extension = Path(filename).suffix.lower().lstrip(".")
    if extension not in settings.allowed_extensions:
        raise ValueError("File type not supported")
