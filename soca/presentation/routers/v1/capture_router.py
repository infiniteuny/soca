from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from soca.config.settings import Settings
from soca.application.capture_camera import CaptureCamera
from soca.injection import settings


capture = APIRouter(
    tags=["capture"],
)


@capture.get("/captures")
def read_all(settings: Annotated[Settings, Depends(settings)]):
    if settings.stream_enabled:
        captures = []
        for camera_id in settings.camera_rtsp_stream_ids:
            captures.append({
                'id': camera_id,
                'url': f'/api/v1/captures/{camera_id}'
            })

        return ORJSONResponse(
            content={
                'status': 'success',
                'data': {
                    'captures': captures
                }
            }
        )
    else:
        return ORJSONResponse(
            status_code=503,
            content={
                'status': 'error',
                'message': 'Captures require the livestreams to be enabled.'
            }
        )


@capture.get("/captures/{id}")
def read(id: str, snashot_camera: Annotated[CaptureCamera, Depends()], settings: Annotated[Settings, Depends(settings)]):
    if settings.stream_enabled:
        try:
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
                        'message': 'Captures require the livestreams to be enabled.'
                    }
                )
            else:
                video = snashot_camera(id)

                return ORJSONResponse(
                    content={
                        'status': 'success',
                        'data': {
                            'capture': {
                                'id': id,
                                'video': video,
                            }
                        }
                    }
                )
        except:
            return ORJSONResponse(
                status_code=500,
                content={
                    'status': 'error',
                    'message': 'Internal server error.'
                }
            )
    else:
        return ORJSONResponse(
            status_code=503,
            content={
                'status': 'error',
                'message': 'Captures require the livestreams to be enabled.'
            }
        )
