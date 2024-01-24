from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from soca.config.settings import Settings
from soca.application.snapshot_camera import SnapshotCamera
from soca.injection import settings


snapshot = APIRouter(
    tags=["snapshot"],
)


@snapshot.get("/snapshots")
def read_all(settings: Annotated[Settings, Depends(settings)]):
    snapshots = []
    for camera_id in settings.camera_rtsps.keys():
        snapshots.append({
            'id': camera_id,
            'url': f'/api/v1/snapshots/{camera_id}'
        })

    return ORJSONResponse(
        content={
            'status': 'success',
            'data': {
                'snapshots': snapshots
            }
        }
    )


@snapshot.get("/snapshots/{id}")
def read(id: str, snashot_camera: Annotated[SnapshotCamera, Depends()], settings: Annotated[Settings, Depends(settings)]):
    try:
        if id in settings.camera_rtsps.keys():
            image = snashot_camera(id)

            return ORJSONResponse(
                content={
                    'status': 'success',
                    'data': {
                        'snapshot': {
                            'id': id,
                            'image': image,
                        }
                    }
                }
            )
        else:
            return ORJSONResponse(
                status_code=404,
                content={
                    'status': 'error',
                    'message': 'Camera not found.'
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
