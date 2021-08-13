import click
import cv2
import numpy as np

from .utils import processor, image_handler


def auto_canny(image, sigma=0.33):
	''' Simple canny edge detector with normalization '''
	v = np.median(image)

	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))

	return cv2.Canny(image, lower, upper)


@click.command('canny')
@processor
def canny_cmd(images):
	''' Highlight edges of an image with canny edge detection '''

	yield from image_handler(images, auto_canny)
