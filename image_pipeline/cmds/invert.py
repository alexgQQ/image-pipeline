import click
import cv2

from .utils import processor, image_handler


@click.command('invert')
@processor
def invert_cmd(images):
    yield from image_handler(images, cv2.bitwise_not, to_cv=True)
