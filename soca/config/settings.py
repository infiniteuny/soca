from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    app_name: str = "Soca"
    app_description: str = "Soca is an API wrapper for a CCTV NVR."
    camera_rtsps: dict[str, str] = {}
    stream_enabled: bool = True
