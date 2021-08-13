import click

from .utils import processor, image_handler


def convert(image, type='RGB'):
    return image.convert(type)


@click.command('convert')
@click.option('-t', '--type', default='average', show_default=True, help='The type of blur to perform')
@processor
def convert_cmd(images, type):
    yield from image_handler(images, convert, type=type)
