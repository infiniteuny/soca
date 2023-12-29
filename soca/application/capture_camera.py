from typing import Annotated
from fastapi import Depends
from soca.domain.repositories.rtsp_repository_abc import RtspRepositoryABC
from soca.infrastructure.repositories.rtsp_repository import RtspRepository


class CaptureCamera:
    rtsp_repository: RtspRepositoryABC

    def __init__(self, rtsp_repository: Annotated[RtspRepository, Depends()]):
        self.rtsp_repository = rtsp_repository

    def __call__(self, camera_id: int) -> str:
        return self.rtsp_repository.capture(camera_id)
