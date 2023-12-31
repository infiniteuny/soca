from fastapi import Depends
from typing import Annotated
from soca.config.settings import Settings
from soca.domain.repositories.rtsp_repository_abc import RtspRepositoryABC
from soca.infrastructure.datasources.rtsp_datasource import RtspDataSource


class RtspRepository(RtspRepositoryABC):
    rtsp_datasource: RtspDataSource

    def __init__(self, rtsp_datasource: Annotated[RtspDataSource, Depends()]):
        self.rtsp_datasource = rtsp_datasource

    def stream(self, camera_id: int) -> None:
        self.rtsp_datasource.stream(camera_id)

    def capture(self, camera_id: int, duration: int = 5) -> str:
        return self.rtsp_datasource.capture(camera_id, duration)

    def snapshot(self, camera_id: int) -> str:
        return self.rtsp_datasource.snapshot(camera_id)
