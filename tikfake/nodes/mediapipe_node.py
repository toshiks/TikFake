import cv2
import mediapipe
import numpy as np


class MediapipeNode:
    def __init__(self):
        """Initialize pose detector."""
        self._pose_detector = mediapipe.solutions.pose.Pose(static_image_mode=False,
                                                            min_detection_confidence=0.5,
                                                            min_tracking_confidence=0.5)

    def reset_state(self):
        """Reset state of node."""
        pass

    def _extract_pose(self, image: np.ndarray):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        return self._pose_detector.process(image)

    @staticmethod
    def _normalize_keypoints(keypoints, image_shape):
        image_rows, image_cols, _ = image_shape

        idx_to_coordinates = {}

        for idx, landmark in enumerate(keypoints.landmark):
            if ((landmark.HasField('visibility') and landmark.visibility < 0.5) or
                    (landmark.HasField('presence') and landmark.presence < 0.5)):
                continue
            landmark_px = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                                                             image_cols, image_rows)
            if landmark_px:
                idx_to_coordinates[idx] = landmark_px

        return idx_to_coordinates

    def process(self, image: np.ndarray):
        """Extract keypoints from image by mediapipe.

        Args:
            image: image in BGR format.

        Returns:
            Array of keypoints
        """
        results = self._extract_pose(image)

        if results is None or results.pose_landmarks is None:
            return None

        return MediapipeNode._normalize_keypoints(results.pose_landmarks, image.shape)
