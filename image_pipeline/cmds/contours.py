import click
import cv2

from .utils import processor, image_handler


def contours(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)

    contours = contours[:20]

    image[:] = 255
    image = cv2.drawContours(image, contours, -1, 0, 1)
    # # image = cv2.bitwise_not(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image


@click.command('contour')
@processor
def contours_cmd(images):
    '''
    Highlight outline of an image
    '''

    yield from image_handler(images, contours, to_cv=True)
