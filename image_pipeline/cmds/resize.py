import click

from .utils import image_handler, processor


def resize(image, width, height):
    return image.resize((width, height))


@click.command('resize')
@click.option('-w', '--width', type=int, help='The new width of the image.')
@click.option('-h', '--height', type=int, help='The new height of the image.')
@processor
def resize_cmd(images, width, height):
    '''
    Resizes an image by fitting it into the box without changing
    the aspect ratio.
    '''
    yield from image_handler(images, resize, width, height)
