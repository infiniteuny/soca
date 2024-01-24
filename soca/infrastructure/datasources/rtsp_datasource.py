from base64 import b64encode
from datetime import datetime
from fastapi import Depends
from soca.config.settings import Settings
from soca.injection import settings
from time import time
from typing import Annotated
from vidgear.gears import CamGear, StreamGear, WriteGear
import cv2
import os


class RtspDataSource:

    def __init__(self, settings: Annotated[Settings, Depends(settings)]) -> None:
        self.settings = settings

    def __construct_rtsp_url(self, camera_id: str) -> None:
        self.rtsp_url = self.settings.camera_rtsps[camera_id]

    def stream(self, camera_id: str) -> None:
        # Construct the RTSP URL
        self.__construct_rtsp_url(camera_id)

        # Construct the output path
        output_path = os.path.join(
            self.settings.app_temp_dir, 'streams', camera_id
        )

        # Create ouput directory if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Open the stream
        source = CamGear(source=self.rtsp_url).start()  # type: ignore

        # Enable livestreaming and retrieve framerate from CamGear Stream and
        # pass it as `-input_framerate` parameter for controlled framerate
        stream_params = {
            '-input_framerate': source.framerate,
            '-livestream': True,
            '-clear_prev_assets': True,
            '-preset': 'ultrafast',
            '-tune': 'zerolatency',
            '-hls_list_size': 3,
            '-hls_delete_threshold': 12,
            '-hls_init_time': 1,
            '-hls_time': 5,
        }

        # Define streamer with manifest-file location and name, format, and
        # other parameters
        streamer = StreamGear(
            output=f'{output_path}/index.m3u8',
            format='hls',
            **stream_params
        )

        while True:
            # Read frames
            frame = source.read()

            if frame is None:
                raise Exception(
                    f'Could not read frame from camera ID {camera_id}.')
            else:
                streamer.stream(frame)

    def capture(self, camera_id: str, duration: int = 5) -> str:
        # Construct the RTSP URL
        self.__construct_rtsp_url(camera_id)

        # Construct the output path
        output_path = os.path.join(self.settings.app_temp_dir, 'captures')
        output_file = os.path.join(output_path, '{camera_id}.mp4')

        # Create ouput directory if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Open the stream
        source = CamGear(source=self.rtsp_url).start()  # type: ignore

        output_params = {
            '-input_framerate': source.framerate,
            '-c:v': 'libx264',
        }

        # Define writer with defined parameters and suitable output filename
        writer = WriteGear(
            output=output_file,
            **output_params  # type: ignore
        )

        end_time = time() + duration + 1
        while time.time() < end_time:
            # Read frames
            frame = source.read()

            # Save the frame
            writer.write(frame)

        # Safely close video stream
        source.stop()

        # Safely close writer
        writer.close()

        with open(output_file, 'rb') as video_file:
            encoded_video = b64encode(video_file.read())

        return encoded_video.decode('utf-8')

    def snapshot(self, camera_id: str) -> str:
        # Construct the RTSP URL
        self.__construct_rtsp_url(camera_id)

        # Open the stream
        source = CamGear(source=self.rtsp_url).start()  # type: ignore

        # Read frames
        frame = source.read()

        if frame is None:
            raise Exception(
                f'Could not read frame from camera ID {camera_id}.')

        # Encode the frame
        _, image_array = cv2.imencode('.jpg', frame)
        encoded_image = b64encode(image_array.tobytes())

        # Safely close video stream
        source.stop()

        return encoded_image.decode('utf-8')
