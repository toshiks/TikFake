from typing import Dict
import pathlib
import csv
from typing import Tuple

from PIL import Image
import cv2
import math
import numpy as np


class SpriteNode:
    def __init__(self):
        self._path = None
        self._part_keypoints = None

    def reset_state(self):
        """Reset state of node."""

    def setup(self, path_to_sprite: pathlib.Path):
        self._path = path_to_sprite
        self._part_keypoints = self._parse_keypoints(path_to_sprite)

    def _parse_keypoints(self, path_to_sprite: pathlib.Path) -> Dict:
        parts = {}
        with open(path_to_sprite / 'keypoints.csv') as keypoints:
            for bodypart in csv.reader(keypoints):
                name, a, b, *_ = bodypart
                parts[name] = {'index': [a, b], 'points': []}
                with open(path_to_sprite / f'{name}.csv') as part:
                    for point in csv.reader(part):
                        parts[name]['points'].append(np.array(point))
        return parts

    def process(self, keypoints: Dict, image: np.ndarray):
        """Drawing sprite bodyparts by keypoints."""
        # image = Image.new("RGBA", shape[:2])
        # image.paste((200, 200, 200), [0, 0, shape[0], shape[1]])
        image = Image.fromarray(image.astype('uint8'), 'RGB')
        head = Image.open("sprites/head.png").rotate(10)
        R, G, B, A = head.split()
        head = Image.merge('RGBA', (B, G, R, A))
        image.paste(head, (100, 200), head)

        # image.save("kek.png")
        return np.array(image)
        # # return np.array(image.convert("RGB"))
        # return cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
