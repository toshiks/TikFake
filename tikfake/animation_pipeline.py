import pathlib

from tikfake.nodes import InputStreamNode, MediapipeNode, RenderingNode, SpriteNode
import cv2


class AnimationPipeline:
    def __init__(self):
        """Initialize pipeline."""
        self._input_node = InputStreamNode()
        self._mediapipe_node = MediapipeNode()
        self._rendering_node = RenderingNode()
        self._sprite_node = SpriteNode()

    def _reset_state(self):
        """Reset state of all pipeline."""
        self._input_node.reset_state()
        self._mediapipe_node.reset_state()
        self._rendering_node.reset_state()
        self._sprite_node.reset_state()

    def _setup(self, path_to_sprite: pathlib.Path):
        self._input_node.setup()
        self._sprite_node.setup(path_to_sprite)

    def process(self, path_to_sprite: pathlib.Path):
        """Create animation from video.

        Args:
            path_to_video: path to mp4 video of tik-tok
            path_to_sprite: path to directory with sprite bodyparts
            path_for_saving: path to mp4 video for saving animation

        Returns:

        """
        self._setup(path_to_sprite)

        while True:
            exist_frame, frame = self._input_node.process()
            if not exist_frame:
                break

            keypoints = self._mediapipe_node.process(frame)
            new_frame = self._rendering_node.process(keypoints, frame, self._sprite_node)
            cv2.imshow('image', new_frame)
            if cv2.waitKey(5) == 13:
                break

        self._reset_state()

    def close(self):
        """Close pipeline."""
        self._reset_state()
