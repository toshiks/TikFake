import pathlib
import sys

from tikfake.animation_pipeline import AnimationPipeline


def main():
    sprite_path = sys.argv[1]
    animation_pipeline = AnimationPipeline()
    animation_pipeline.process(pathlib.Path(sprite_path))


if __name__ == '__main__':
    main()
