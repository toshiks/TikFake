import logging
import pathlib
from typing import Optional

import cv2
import numpy as np


class SaveVideoNode:
    """Node for saving node by each frame"""

    _logger = logging.getLogger("SaveVideoNode")

    def __init__(self):
        """Init function."""
        self._video_writer: Optional[cv2.VideoWriter] = None
        self._image_shape: Optional[np.ndarray] = None
        self._video_save_path: Optional[pathlib.Path] = None

    def reset_state(self):
        """Reset state of node."""
        self.close()
        self._video_writer = None
        self._image_shape = None
        self._video_save_path = None

    def setup(self, path_for_saving: pathlib.Path, fps: int, image_width: int, image_height: int):
        """Setup video writer.

        Args:
            path_for_saving: path to disk for saving mp4 video
            fps: fps of output video
            image_width: width of output video
            image_height: height of output video
        """
        self._video_writer = cv2.VideoWriter(
            str(path_for_saving),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (image_width, image_height)
        )

        self._image_shape = (image_width, image_height)
        self._video_save_path = path_for_saving
        self._logger.info("Created video safer")

    def process(self, image_frame: np.ndarray):
        """Process function."""
        if not self._video_writer:
            return

        if image_frame.shape[0] != self._image_shape[0] or image_frame[1] != self._image_shape[1]:
            image_frame = cv2.resize(image_frame, self._image_shape)

        self._video_writer.write(image_frame)

    def close(self):
        """Close function."""
        if self._video_writer:
            self._video_writer.release()
            self._logger.info("Saved video to %s", self._video_save_path)
