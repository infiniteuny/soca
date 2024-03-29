from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, ORJSONResponse
from soca.config.settings import Settings
from soca.injection import settings
import os


livestream = APIRouter(
    tags=["livestream"],
)


@livestream.get("/livestreams")
def read_all(settings: Annotated[Settings, Depends(settings)]):
    if settings.stream_enabled:
        livestreams = []
        for camera_id in settings.camera_rtsp_stream_ids:
            livestreams.append({
                'id': camera_id,
                'url': f'/api/v1/livestreams/{camera_id}/index'
            })

        return ORJSONResponse(
            content={
                'status': 'success',
                'data': {
                    'livestreams': livestreams
                }
            }
        )
    else:
        return ORJSONResponse(
            status_code=503,
            content={
                'status': 'error',
                'message': 'Livestreams disabled.'
            }
        )


@livestream.get("/livestreams/{id}")
def read(id: str, settings: Annotated[Settings, Depends(settings)]):
    if settings.stream_enabled:
        if id not in settings.camera_rtsp_ids:
            return ORJSONResponse(
                status_code=404,
                content={
                    'status': 'error',
                    'message': 'Camera not found.'
                }
            )
        elif id not in settings.camera_rtsp_stream_ids:
            return ORJSONResponse(
                status_code=503,
                content={
                    'status': 'error',
                    'message': 'Livestreams disabled.'
                }
            )
        else:
            return ORJSONResponse(
                content={
                    'status': 'success',
                    'data': {
                        'livestream': {
                            'id': id,
                            'url': f'/api/v1/livestreams/{id}/index'
                        }
                    }
                }
            )
    else:
        return ORJSONResponse(
            status_code=503,
            content={
                'status': 'error',
                'message': 'Livestreams disabled.'
            }
        )


@livestream.get("/livestreams/{id}/{filename}")
def read_blob(id: str, filename: str, settings: Annotated[Settings, Depends(settings)]):
    if settings.stream_enabled:
        static_file_path = os.path.join(settings.app_temp_dir, 'streams', id)
        if filename == 'index' and os.path.isfile(os.path.join(static_file_path, f'{filename}.m3u8')):
            return FileResponse(os.path.join(static_file_path, f'{filename}.m3u8'))
        elif filename.endswith('.ts') and os.path.isfile(os.path.join(static_file_path, filename)):
            return FileResponse(os.path.join(static_file_path, filename))
        else:
            return ORJSONResponse(
                status_code=404,
                content={
                    'status': 'error',
                    'message': 'File not found.'
                }
            )
    else:
        return ORJSONResponse(
            status_code=503,
            content={
                'status': 'error',
                'message': 'Livestreams disabled.'
            }
        )
