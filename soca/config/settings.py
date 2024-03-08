import os
import tempfile
from pydantic import validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    app_name: str = "Soca"
    app_description: str = "Soca is an API wrapper for a CCTV NVR."
    app_temp_dir: str = os.path.join(tempfile.gettempdir(), "soca")
    camera_rtsps: list[dict[str, str | bool]] = []
    camera_rtsp_ids: list[str] = []
    camera_rtsp_stream_ids: list[str] = []
    stream_enabled: bool = True

    @validator('camera_rtsp_ids', pre=True)
    def compute_camera_rtsp_ids(cls, v, values):
        camera_rtsps = values.get('camera_rtsps')
        return [camera_rtsp['id'] for camera_rtsp in camera_rtsps]

    @validator('camera_rtsp_stream_ids', pre=True)
    def compute_camera_rtsp_stream_ids(cls, v, values):
        camera_rtsps = values.get('camera_rtsps')
        return [
            camera_rtsp['id'] for camera_rtsp in camera_rtsps if camera_rtsp['stream_enabled'] == True
        ]
