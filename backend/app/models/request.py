from datetime import datetime

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    upload_id: str = Field(min_length=1)


class UploadMetadata(BaseModel):
    label: str | None = None
    recorded_at: datetime | None = None
