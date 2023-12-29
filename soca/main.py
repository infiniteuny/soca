from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
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
    if settings().stream_enabled:
        streams: dict[int, StreamCamera] = {}
        for camera_id in settings().camera_ids:
            rtsp_datasource = RtspDataSource(settings())
            rtsp_repository = RtspRepository(rtsp_datasource)
            streams[camera_id] = StreamCamera(camera_id, rtsp_repository)
            streams[camera_id].start()
    yield

# Core application instance
app = FastAPI(
    title=settings().app_name,
    description=settings().app_description,
    redoc_url=None,
    lifespan=lifespan,
)

# API router
api = APIRouter(
    prefix="/api",
)

# Add API router
api.include_router(livestream, prefix="/v1")
api.include_router(capture, prefix="/v1")
api.include_router(snapshot, prefix="/v1")
app.include_router(api)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
