from typing import Dict, Optional

import cv2
import numpy as np
from mediapipe.python.solutions.pose import POSE_CONNECTIONS


class RenderingNode:
    def __init__(self):
        pass

    def reset_state(self):
        """Reset state of node."""

    def _render_skeleton(self, keypoints: Dict, image: np.ndarray):
        for connection in POSE_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            if start_idx in keypoints and end_idx in keypoints:
                cv2.line(image, keypoints[start_idx], keypoints[end_idx], (0, 255, 0), 2)

        for landmark_px in keypoints.values():
            cv2.circle(image, landmark_px, 2, (0, 0, 255), 2)

    def process(self, keypoints: Optional[Dict], image: np.ndarray) -> np.ndarray:
        """Drawing image by keypoints.

        Args:
            keypoints: dict of keypoints. If null will be used previous sample or default.
            image: image in BGR format where keypoints were

        Returns:
            Rendered image.
        """

        image = cv2.flip(image, 1)

        if keypoints is not None:
            self._render_skeleton(keypoints, image)

        return image
