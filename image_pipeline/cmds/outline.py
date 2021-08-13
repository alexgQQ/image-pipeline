import click
import cv2

from .utils import processor, image_handler


def outline(image):
    image[image[:, :, 3] != 0] = 255
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image[:] = 255
    return cv2.drawContours(image, contours, -1, 0, 1)


@click.command('outline')
@processor
def outline_cmd(images):
    ''' Highlight outline of an image '''
    yield from image_handler(images, outline, to_cv=True)
