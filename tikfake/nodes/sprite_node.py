from typing import Dict
import pathlib
import csv
from typing import Tuple

from PIL import Image, ImageDraw, ImageOps
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
                parts[name] = {'index': [int(a), int(b)], 'points': []}

                R, G, B, A = Image.open(path_to_sprite / f'{name}.png').split()
                image = Image.merge('RGBA', (B, G, R, A))
                width, height = image.size[:2]
                pad = max(width, height)
                image = ImageOps.expand(image, pad)
                parts[name]['image'] = image
                delta = np.array([pad, pad])

                with open(path_to_sprite / f'{name}.csv') as part:
                    for point in csv.reader(part):
                        parts[name]['points'].append(np.array(list(map(int, point))) + delta)

                # point_a, point_b, *_ = parts[name]['points']
                # draw = ImageDraw.Draw(image)
                # draw.line((point_a[0], point_a[1], point_b[0], point_b[1]), width=4, fill='blue')
                # image.save(f'image_{name}.png')
        return parts

    @staticmethod
    def _angle(v1, v2):
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        return math.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

    @staticmethod
    def _scale(v1, v2):
        return np.linalg.norm(v2) / np.linalg.norm(v1)

    def _render_single_sprite(self, keypoints: Dict, bodypart: str, image: Image):
        """Draw a single sprite on top of the image."""
        index_a, index_b = self._part_keypoints[bodypart]['index']
        point_a, point_b, *_ = self._part_keypoints[bodypart]['points']
        kp_a = keypoints.get(index_a)
        kp_b = keypoints.get(index_b)

        if kp_a is None or kp_b is None:
            return

        kp_a = np.array(kp_a)
        kp_b = np.array(kp_b)

        scale = self._scale(point_b - point_a, kp_b - kp_a)
        angle = self._angle(point_b - point_a, kp_b - kp_a)
        cx, cy = int(scale * point_a[0]), int(scale * point_a[1])
        dx, dy = int(kp_a[0] - cx), int(kp_a[1] - cy)

        sprite = self._part_keypoints[bodypart]['image'].copy()

        width = int(sprite.size[0] * scale)
        height = int(sprite.size[1] * scale)
        if not width or not height:
            return

        # draw = ImageDraw.Draw(sprite)
        # draw.line((point_a[0], point_a[1], point_b[0], point_b[1]), width=3, fill='blue')

        sprite = sprite.resize((width, height), Image.ANTIALIAS)
        sprite = sprite.rotate(angle, center=(cx, cy))

        # draw = ImageDraw.Draw(sprite)
        # draw.line((cx, cy, cx+1, cy+1), width=10, fill='red')
        # draw.line((center[0], center[1], center[0]+1, center[1]+1), width=10, fill='yellow')

        # sprite.save(f'sprite_{bodypart}.png')
        image.paste(sprite, (dx, dy), sprite)
        # image.save(f'frame_{bodypart}.png')

        # draw = ImageDraw.Draw(image)
        # draw.line((kp_a[0], kp_a[1], kp_b[0], kp_b[1]), width=3, fill='red')
        # draw.line((dx, dy, dx+1, dy+1), width=10, fill='red')

    def process(self, keypoints: Dict, image: np.ndarray):
        """Drawing sprite bodyparts by keypoints."""
        # image = Image.new("RGBA", (image.shape[1], image.shape[0]), color='white')
        image = Image.fromarray(image.astype('uint8'), 'RGB')

        for bodypart in self._part_keypoints:
            self._render_single_sprite(keypoints, bodypart, image)

        # return cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
        return np.array(image)
