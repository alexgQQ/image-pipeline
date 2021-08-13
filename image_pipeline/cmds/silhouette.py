import click
import cv2

from .utils import image_handler, processor


def silhouette(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # image[:] = 255
    # image = cv2.drawContours(image, contours, -1, 0, 1)
    outline = cv2.bitwise_not(image)
    contours, _ = cv2.findContours(outline, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)
    outline_mask =  cv2.drawContours(outline, contours, 0, 255, cv2.FILLED)
    outline = cv2.cvtColor(cv2.bitwise_not(outline_mask), cv2.COLOR_GRAY2RGB)
    return outline


@click.command('silhouette')
@processor
def silhouette_cmd(images):
    ''' Highlight outline of an image '''
    yield from image_handler(images, silhouette, to_cv=True)
