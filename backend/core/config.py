from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Vireon - Quick Learn MVP"
    ENVIRONMENT: str = "local"
    
    # Storage Config
    STORAGE_DIR: str = "storage"
    UPLOAD_DIR: str = f"{STORAGE_DIR}/uploads"
    COURSE_DIR: str = f"{STORAGE_DIR}/courses"
    
    # Model Config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_LLM_MODEL: str = "llama3"

    class Config:
        env_file = ".env"

settings = Settings()
