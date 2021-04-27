import logging
import pathlib
from typing import Tuple

import cv2
import numpy as np


class InputStreamNode:
    """Input stream node for video."""

    _logger = logging.getLogger("InputNode")

    def __init__(self):
        """Init function."""
        self._stream = None

    def reset_state(self):
        """Reset state of node."""
        self._stream = None

    def setup(self, path_to_video: pathlib.Path):
        """Setup function.

        Args:
            path_to_video : path to video with tik-tok.
        """

        string_path_to_video = str(path_to_video)

        self._stream = cv2.VideoCapture(string_path_to_video)

        if not self._stream.isOpened() or not self._get_frame()[0]:
            self._stream.release()
            self._logger.error("Cannot open video from: %s", string_path_to_video)

        self._logger.info("Opened stream: %s", string_path_to_video)

    @property
    def stream_fps(self) -> int:
        return int(self._stream.get(cv2.CAP_PROP_FPS))

    @property
    def stream_width(self) -> int:
        return int(self._stream.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def stream_height(self) -> int:
        return int(self._stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def _get_frame(self) -> Tuple[bool, np.ndarray]:
        """Get frame function.

        Returns:
            success: is available image or not.
            image: image from stream.
        """
        success, image = self._stream.read()
        return success, image

    def process(self) -> Tuple[bool, np.ndarray]:
        """Process function for getting stream."""
        return self._get_frame()

    def close(self):
        """Close function."""
        self._stream.release()
