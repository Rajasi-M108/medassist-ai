"""
Central app configuration, loaded from environment variables / .env.

Using pydantic-settings means every other module imports a single
`settings` object instead of scattering os.environ.get() calls around
the codebase -- and it validates types (e.g. ACCESS_TOKEN_EXPIRE_MINUTES
really is an int) at startup instead of failing weirdly at runtime.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    DATABASE_URL: str = "sqlite:///./medassist.db"

    # Auth
    JWT_SECRET_KEY: str = "dev-only-insecure-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # File storage
    UPLOAD_DIR: str = "./uploads"

    # AI provider
    AI_PROVIDER: str = "stub"
    AI_API_KEY: str = ""

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"


settings = Settings()
