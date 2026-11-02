
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    APP_NAME: str = "MCP AI Agent"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # LLM
    LLM_PROVIDER: str = "groq"

    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    GROQ_MODEL: str = "openai/gpt-oss-120b"
    OPENAI_MODEL: str = "gpt-4o-mini"

    # MCP servers
    WEATHER_MCP_URL: str = "http://127.0.0.1:8001/mcp"
    FINANCE_MCP_URL: str = "http://127.0.0.1:8002/mcp"
    DATABASE_MCP_URL: str = "http://127.0.0.1:8003/mcp"

    MCP_TIMEOUT: int = Field(
        default=30,
        gt=0,
        le=300
    )

    @property
    def MCP_SERVERS(self):
        return {
            "weather": self.WEATHER_MCP_URL,
            "finance": self.FINANCE_MCP_URL,
            "database": self.DATABASE_MCP_URL
        }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
