from typing import Dict
import pathlib
import csv
from typing import Tuple

from PIL import Image, ImageDraw, ImageOps, ImageFilter
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
                name, *indices = bodypart
                parts[name] = {'index': list(map(int, indices)), 'points': []}

                image = Image.open(path_to_sprite / f'{name}.png')
                width, height = image.size[:2]
                pad = max(width, height)
                image = ImageOps.expand(image, pad)
                parts[name]['image'] = image
                delta = np.array([pad, pad])

                with open(path_to_sprite / f'{name}.csv') as part:
                    for point in csv.reader(part):
                        parts[name]['points'].append(np.array(list(map(int, point))) + delta)

        return parts

    @staticmethod
    def _angle(v1, v2):
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        sin = np.cross(v2, v1)
        cos = np.dot(v2, v1)
        return np.rad2deg(np.arctan2(sin, cos))

    @staticmethod
    def _scale(v1, v2):
        return np.linalg.norm(v2) / np.linalg.norm(v1)

    def _get_height_scale(self, keypoints: Dict, bodypart: str) -> int:
        point_a, point_b, point_c, point_d, *_ = self._part_keypoints[bodypart]['points']
        kp_a, kp_b, kp_c, kp_d, *_ = map(keypoints.get, self._part_keypoints[bodypart]['index'])
        if None in [kp_a, kp_b, kp_c, kp_d]:
            return None
        kp_a, kp_b, kp_c, kp_d = map(np.array, [kp_a, kp_b, kp_c, kp_d])
        return self._scale((point_a + point_b) / 2 - (point_c + point_d) / 2,
                           (kp_a + kp_b) / 2 - (kp_c + kp_d) / 2)

    def _render_single_sprite(self, keypoints: Dict, bodypart: str, image: Image):
        """Draw a single sprite on top of the image."""
        index_a, index_b, *indices = self._part_keypoints[bodypart]['index']
        point_a, point_b, *points = self._part_keypoints[bodypart]['points']
        kp_a, kp_b = keypoints.get(index_a), keypoints.get(index_b)

        if kp_a is None or kp_b is None:
            return

        kp_a, kp_b = np.array(kp_a), np.array(kp_b)

        scale_x = scale_y = self._scale(point_b - point_a, kp_b - kp_a)
        sprite = self._part_keypoints[bodypart]['image'].copy()

        if indices:
            scale = self._get_height_scale(keypoints, bodypart)
            if scale is not None:
                scale_y = scale

        width = int(sprite.size[0] * scale_x)
        height = int(sprite.size[1] * scale_y)
        if not width or not height:
            return

        angle = self._angle(point_b - point_a, kp_b - kp_a)
        cx, cy = int(scale_x * point_a[0]), int(scale_y * point_a[1])
        dx, dy = int(kp_a[0] - cx), int(kp_a[1] - cy)

        # draw = ImageDraw.Draw(sprite)
        # draw.line((point_a[0], point_a[1], point_b[0], point_b[1]), width=3, fill='blue')

        sprite = sprite.resize((width, height), Image.ANTIALIAS)
        sprite = sprite.rotate(angle, center=(cx, cy))
        image.paste(sprite, (dx, dy), sprite)

        # draw = ImageDraw.Draw(image)
        # draw.line((kp_a[0], kp_a[1], kp_b[0], kp_b[1]), width=3, fill='red')

    def process(self, keypoints: Dict, image: np.ndarray):
        """Drawing sprite bodyparts by keypoints."""
        # image = Image.new("RGBA", (image.shape[1], image.shape[0]), color='white')

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image.astype('uint8'), 'RGB').filter(ImageFilter.BoxBlur(1000))

        if keypoints is not None:
            for bodypart in self._part_keypoints:
                self._render_single_sprite(keypoints, bodypart, image)

        return cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
