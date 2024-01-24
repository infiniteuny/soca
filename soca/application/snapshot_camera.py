from typing import Annotated
from fastapi import Depends
from soca.domain.repositories.rtsp_repository_abc import RtspRepositoryABC
from soca.infrastructure.repositories.rtsp_repository import RtspRepository


class SnapshotCamera:
    rtsp_repository: RtspRepositoryABC

    def __init__(self, rtsp_repository: Annotated[RtspRepository, Depends()]):
        self.rtsp_repository = rtsp_repository

    def __call__(self, camera_id: str) -> str:
        return self.rtsp_repository.snapshot(camera_id)
