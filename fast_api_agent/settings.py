from pydantic_settings import BaseSettings, SettingsConfigDict

class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config.cfg")

    model: str
    db_url: str | None = None
