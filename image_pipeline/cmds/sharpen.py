import click

from .utils import processor, image_handler
from PIL import ImageEnhance


def sharpen(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(max(1.0, factor))


@click.command('sharpen')
@click.option(
    '-f', '--factor', default=2.0, help='Sharpens the image.', show_default=True
)
@processor
def sharpen_cmd(images, factor):
    ''' Sharpens an image. '''
    yield from image_handler(images, sharpen, factor)
