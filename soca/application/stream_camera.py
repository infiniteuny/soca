from datetime import datetime
from fastapi import Depends
from soca.domain.repositories.rtsp_repository_abc import RtspRepositoryABC
from soca.infrastructure.repositories.rtsp_repository import RtspRepository
from threading import Event, Thread
from time import sleep
from typing import Annotated


class StreamCamera(Thread):
    id: str
    stop_event: Event
    rtsp_repository: RtspRepositoryABC

    def __init__(self, id: str, stop_event: Event, rtsp_repository: Annotated[RtspRepository, Depends()]):
        Thread.__init__(self)
        self.id = id
        self.stop_event = stop_event
        self.rtsp_repository = rtsp_repository

    def run(self, *args, **kwargs):
        print(
            '{} :: Camera {} Thread :: Starting...'.format(
                datetime.now().strftime('%H:%M:%S'),
                str(self.id),
            )
        )

        while not self.stop_event.is_set():
            try:
                self.rtsp_repository.stream(self.id)
            except BaseException as error:
                sleep(1)
                if not self.stop_event.is_set():
                    if str(error):
                        message = str(error)
                    else:
                        message = 'Unknown error occured!'
                    print(
                        '{} :: Camera {} Thread :: {}'.format(
                            datetime.now().strftime('%H:%M:%S'),
                            str(self.id),
                            message,
                        )
                    )
                sleep(4)
                continue
            except:
                print(
                    '{} :: Camera {} Thread :: Unknown error occured!'.format(
                        datetime.now().strftime('%H:%M:%S'),
                        str(self.id),
                    )
                )
                sleep(5)
                continue

        print(
            '{} :: Camera {} Thread :: Shutting down...'.format(
                datetime.now().strftime('%H:%M:%S'),
                str(self.id),
            )
        )
