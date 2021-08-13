"""
General code to provide blurring operations to images.

Reference: https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
"""

import click
import cv2

from .utils import processor, image_handler


def blur(image, type='average', k=3):
    if type == 'gaussian':
        return cv2.GaussianBlur(image, (k, k), 0)
    elif type == 'median':
        return cv2.medianBlur(image, k)
    return cv2.blur(image, (k, k))


@click.command('blur')
@click.option('-t', '--type', default='average', show_default=True, help='The type of blur to perform')
@click.option('-k', '--kernel', default=3, show_default=True, help='The kernel size for convolution, must be an odd number, typically 3, 5, 7, 11.')
@processor
def blur_cmd(images, type, kernel):
    ''' Applies various blur operations to an image. '''
    print('foobar')
    yield from image_handler(images, blur, to_cv=True, type=type, k=kernel)
