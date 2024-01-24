from contextlib import asynccontextmanager
from threading import Event
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from soca.application.stream_camera import StreamCamera
from soca.infrastructure.datasources.rtsp_datasource import RtspDataSource
from soca.infrastructure.repositories.rtsp_repository import RtspRepository
from soca.injection import settings
from soca.presentation.routers.v1.livestream_router import livestream
from soca.presentation.routers.v1.capture_router import capture
from soca.presentation.routers.v1.snapshot_router import snapshot
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    streams: dict[str, StreamCamera] = {}
    stop_events: dict[str, Event] = {}
    if settings().stream_enabled:
        for camera_id, _ in settings().camera_rtsps.items():
            rtsp_datasource = RtspDataSource(settings())
            rtsp_repository = RtspRepository(rtsp_datasource)
            stop_events[camera_id] = Event()
            streams[camera_id] = StreamCamera(
                camera_id,
                stop_events[camera_id],
                rtsp_repository
            )
            streams[camera_id].start()
    yield
    if settings().stream_enabled:
        for camera_id, _ in settings().camera_rtsps.items():
            stop_events[camera_id].set()
        for camera_id, _ in settings().camera_rtsps.items():
            streams[camera_id].join()

# Core application instance
app = FastAPI(
    title=settings().app_name,
    description=settings().app_description,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# API router
api = APIRouter(
    prefix='/api',
)

# Add API router
api.include_router(livestream, prefix='/v1')
api.include_router(capture, prefix='/v1')
api.include_router(snapshot, prefix='/v1')
app.include_router(api)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
