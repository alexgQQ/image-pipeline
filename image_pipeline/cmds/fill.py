import click
import cv2

from .utils import processor, image_handler


def fill(image):
    ret, mask = cv2.threshold(image[:, :, 3], 0, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGBA)
    return cv2.bitwise_and(image, mask)


@click.command('fill')
@processor
def fill_cmd(images):
    yield from image_handler(images, fill, to_cv=True)
