import click
import cv2
import numpy as np

from .utils import processor, image_handler


def threshold(image, c_size=15, offset=6):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    v = np.average(image)
    _max = np.max(image)
    sigma = 0.333
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    # ret, image = cv2.threshold(image, upper, _max, 0)
    image = cv2.adaptiveThreshold(image, _max, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, c_size, offset)
    # _, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    # image = cv2.bitwise_not(image)
    # kernel = np.ones((3, 3), np.uint8)
    # image = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
    # image = cv2.bitwise_not(image)
    return image


@click.command('threshold')
@processor  
def threshold_cmd(images):
    yield from image_handler(images, threshold)
