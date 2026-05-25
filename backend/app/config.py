from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 1. Variabel utama yang wajib buat Workflow Roboflow
    ROBOFLOW_API_KEY: str
    ROBOFLOW_WORKSPACE: str
    ROBOFLOW_WORKFLOW: str

    # 2. Variabel ekstra dari .env lu (kita daftarin semua biar Pydantic tenang)
    ROBOFLOW_PROJECT: Optional[str] = None
    ROBOFLOW_VERSION: Optional[str] = None
    APP_ENV: Optional[str] = None
    APP_HOST: Optional[str] = None
    APP_PORT: Optional[str] = None
    ALLOWED_ORIGINS: Optional[str] = None
    MAX_VIDEO_SIZE_MB: Optional[str] = None
    UPLOAD_DIR: Optional[str] = None
    ANALYSIS_TIMEOUT_SECONDS: Optional[str] = None

    # Konfigurasi pembacaan file .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # Biar huruf besar/kecil di .env gak sensitif
    )

settings = Settings()