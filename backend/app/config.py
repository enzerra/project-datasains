from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Traffic Congestion Predictor API"
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    allowed_origins: str = Field(default="http://localhost:3000", alias="ALLOWED_ORIGINS")
    roboflow_api_key: str = Field(default="", alias="ROBOFLOW_API_KEY")
    roboflow_api_url: str = Field(default="https://serverless.roboflow.com", alias="ROBOFLOW_API_URL")
    roboflow_project_id: str = Field(default="", alias="ROBOFLOW_PROJECT_ID")
    roboflow_model_version: str = Field(default="1", alias="ROBOFLOW_MODEL_VERSION")
    roboflow_workspace: str = Field(default="", alias="ROBOFLOW_WORKSPACE")
    roboflow_workflow_id: str = Field(default="", alias="ROBOFLOW_WORKFLOW_ID")
    max_video_size_mb: int = Field(default=100, alias="MAX_VIDEO_SIZE_MB")
    upload_dir: str = Field(default="./tmp/uploads", alias="UPLOAD_DIR")
    allowed_video_extensions: str = Field(default="mp4,avi,mov,mkv,webm", alias="ALLOWED_VIDEO_EXTENSIONS")
    frames_per_second: int = Field(default=1, alias="FRAMES_PER_SECOND")
    max_frames_to_analyze: int = Field(default=30, alias="MAX_FRAMES_TO_ANALYZE")
    analysis_timeout_seconds: int = Field(default=120, alias="ANALYSIS_TIMEOUT_SECONDS")

    @property
    def allowed_extensions(self) -> set[str]:
        return {ext.strip().lower() for ext in self.allowed_video_extensions.split(",") if ext.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
