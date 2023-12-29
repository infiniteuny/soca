from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Soca"
    app_description: str = "Soca is an API wrapper for a CCTV NVR."
    rtsp_host: str = "localhost"
    rtsp_port: int = 554
    rtsp_username: str
    rtsp_password: str
    camera_ids: list = [1, 2, 3]
    stream_enabled: bool = True
