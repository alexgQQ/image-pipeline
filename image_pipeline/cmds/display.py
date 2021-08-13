import click
import cv2
from functools import wraps

from .utils import processor, image_handler


def display(image, width, height):
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    yield image


@click.command('display')
@processor
def display_cmd(images):
    ''' Opens all images in an image viewer. '''
    yield from image_handler(images, display, to_cv=True)
