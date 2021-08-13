#!/home/agent/.cache/pypoetry/virtualenvs/image-pipeline-Z3U06Al4-py3.8/bin/python

import click
import cv2
import glob
import os
import re

from PIL import Image

from cmds import commands
from cmds.utils import processor, generator


@click.group(chain=True)
def cli():
    """
    This script processes a bunch of images through pillow in a unix
    pipe.  One commands feeds into the next.

    Example:

    \b
        imagepipe open -i example01.jpg resize -w 128 display
        imagepipe open -i example02.jpg blur save
    """


@cli.resultcallback()
def process_commands(processors):
    """
    This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    stream = ()

    for processor in processors:
        stream = processor(stream)

    for data in stream:
        data


def run():
    for cmd in commands:
        cli.add_command(cmd)
    cli()


def scan_dir(dir_path):
    """
    Gather all image files under a single level directory
    """
    pattern = '.*\.(jpeg|png|jpg|svg)$'
    image_paths = (path for path in glob.glob(os.path.join(dir_path, '*')) if re.search(pattern, path))
    for path in image_paths:
        yield path


@cli.command("open")
@click.option(
    "-i", "--image", "images",
    type=click.Path(exists=True),
    multiple=True,
    help="The source for the image data. Can be a file, directory, url or stdin.",
)
@click.option(
    "-r", "--repeat",
    type=int, default=1,
    help="Reload each image the given number of times.",
)
@generator
def open_cmd(images, repeat):
    """
    Loads one or multiple images for processing.  The input parameter
    can be specified multiple times to load more than one image.
    """
    for image in images:
        try:
            click.echo(f"Opening '{image}'")
            if image == '-':
                img = Image.open(click.get_binary_stdin())
                img.filename = '-'
                yield img
            elif os.path.isdir(image):
                for path in scan_dir(image):
                    yield Image.open(path)
            else:
                for _ in range(repeat):
                    yield Image.open(image)
        except Exception as e:
            click.echo(f"Could not open image '{image}': {e}", err=True)


@cli.command('save')
@click.option(
    '--filename',
    default='processed-{:04}.png',
    type=click.Path(),
    help='The format for the filename.',
    show_default=True,
)
@processor
def save_cmd(images, filename):
    ''' Saves all processed images to a series of files. '''
    pattern = '.*\.(jpeg|png|jpg|svg)$'
    to_file = bool(re.search(pattern, filename))
    dirname = os.path.dirname(filename) if to_file else filename
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    for idx, image in enumerate(images):
        try:
            if not to_file:
                fn = os.path.join(dirname, os.path.basename(image.filename))
            else:
                fn = filename.format(idx + 1)
            click.echo(f"Saving '{image.filename}' as '{fn}'")
            image.save(fn)
            yield image
        except Exception as e:
            click.echo(f"Could not save image '{image.filename}': {e}", err=True)


if __name__ == '__main__':
    run()
