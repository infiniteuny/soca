from contextlib import asynccontextmanager
import shutil
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
    shutil.rmtree(settings().app_temp_dir, ignore_errors=True)

    streams: dict[str, StreamCamera] = {}
    stop_events: dict[str, Event] = {}
    if settings().stream_enabled:
        for camera_id in settings().camera_rtsp_stream_ids:
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
        for camera_id in settings().camera_rtsp_stream_ids:
            stop_events[camera_id].set()
        for camera_id in settings().camera_rtsp_stream_ids:
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


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return ORJSONResponse(
        status_code=404,
        content={
            'status': 'error',
            'message': 'Not found.'
        }
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
    uvicorn.run(app, host='0.0.0.0', port=8000, server_header=False)
