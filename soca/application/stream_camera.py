from fastapi import Depends
from soca.domain.repositories.rtsp_repository_abc import RtspRepositoryABC
from soca.infrastructure.repositories.rtsp_repository import RtspRepository
from threading import Thread
from typing import Annotated


class StreamCamera(Thread):
    rtsp_repository: RtspRepositoryABC

    def __init__(self, id: int, rtsp_repository: Annotated[RtspRepository, Depends()]):
        Thread.__init__(self)
        self.id = id
        self.rtsp_repository = rtsp_repository

    def run(self, *args, **kwargs):
        while True:
            self.rtsp_repository.stream(self.id)
