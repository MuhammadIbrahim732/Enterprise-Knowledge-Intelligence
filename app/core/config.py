from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Knowledge Intelligence"

    DEBUG: bool = True

    GEMINI_API_KEY: str

    LLM_MODEL: str = "gemini-3.5-flash-lite"

    EMBEDDING_MODEL: str = "gemini-embedding-001"

    EMBEDDING_DIMENSION: int = 768

    UPLOAD_DIR: str = "data/uploads"

    CHROMA_DIR: str = "data/chroma_db"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )


settings = Settings()
