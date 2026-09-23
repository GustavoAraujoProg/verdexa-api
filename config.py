from pathlib import Path
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    database_url: str = 'sqlite:///./verdexa.db'
    jwt_secret: str = Field(min_length=32)
    token_minutes: int = Field(default=60, ge=1, le=1440)
    upload_dir: Path = Path('uploads')
    max_upload_mb: int = Field(default=10, ge=1, le=30)
    cors_origins: list[str] = []
    ia_url: str | None = None
    ia_api_key: str | None = None
    ia_timeout_seconds: int = Field(default=60, ge=1, le=300)
    ia_min_confidence: float = Field(default=0.7, ge=0, le=1)

    @model_validator(mode='after')
    def validar_url(self):
        if self.ia_url and not self.ia_url.startswith(('http://', 'https://')):
            raise ValueError('IA_URL deve usar http:// ou https://')
        return self


settings = Settings()
