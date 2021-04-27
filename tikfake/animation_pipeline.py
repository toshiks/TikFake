import pathlib

from tikfake.nodes import InputStreamNode, MediapipeNode, RenderingNode, SaveVideoNode


class AnimationPipeline:
    def __init__(self):
        """Initialize pipeline."""
        self._input_node = InputStreamNode()
        self._mediapipe_node = MediapipeNode()
        self._rendering_node = RenderingNode()
        self._save_node = SaveVideoNode()

    def _reset_state(self):
        """Reset state of all pipeline."""
        self._input_node.reset_state()
        self._mediapipe_node.reset_state()
        self._rendering_node.reset_state()
        self._save_node.reset_state()

    def _setup(self, path_to_video: pathlib.Path, path_for_saving: pathlib.Path):
        self._input_node.setup(path_to_video)
        self._save_node.setup(path_for_saving, self._input_node.stream_fps, self._input_node.stream_width,
                              self._input_node.stream_height)

    def process(self, path_to_video: pathlib.Path, path_for_saving: pathlib.Path):
        """Create animation from video.

        Args:
            path_to_video: path to mp4 video of tik-tok
            path_for_saving: path to mp4 video for saving animation

        Returns:

        """
        self._setup(path_to_video, path_for_saving)

        while True:
            exist_frame, frame = self._input_node.process()
            if not exist_frame:
                break

            keypoints = self._mediapipe_node.process(frame)
            new_frame = self._rendering_node.process(keypoints, frame)
            self._save_node.process(new_frame)

        self._reset_state()

    def close(self):
        """Close pipeline."""
        self._reset_state()
