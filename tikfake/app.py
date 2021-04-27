import pathlib

from tikfake.animation_pipeline import AnimationPipeline


def main():
    animation_pipeline = AnimationPipeline()
    animation_pipeline.process(pathlib.Path("/Users/klochkovanton/Downloads/be68149df83e44fdbea64b9a0ca323ac.mp4"),
                               pathlib.Path("output.mp4"))


if __name__ == '__main__':
    main()
