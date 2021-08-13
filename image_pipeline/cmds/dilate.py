import click
import numpy as np
import cv2

from .utils import processor, image_handler


def dilate(image, k=3, iterations=1):
    kernel = np.ones((k, k), np.uint8)
    image = cv2.dilate(image, kernel, cv2.BORDER_CONSTANT, iterations=iterations)
    return image


@click.command('dilate')
@click.option('-k', '--kernel', default=3, help='Kernel size for operation.')
@click.option('-i', '--iterations', default=1, help='How many times to run the operation.')
@processor
def dilate_cmd(images, kernel, iterations):
    yield from image_handler(images, dilate, to_cv=True, k=kernel, iterations=iterations)
