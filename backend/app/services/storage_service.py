from pathlib import Path

from app.config import settings


class StorageService:
    def __init__(self) -> None:
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def build_upload_path(self, upload_id: str, filename: str) -> Path:
        suffix = Path(filename).suffix.lower() or ".jpg"
        return self.upload_dir / f"{upload_id}{suffix}"
