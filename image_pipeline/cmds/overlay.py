import click

from .utils import processor, image_handler


def overlay(image):
    image = image.convert('RGBA')
    datas = image.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    return image


@click.command("overlay")
@click.option(
    "-f", "--file",
    type=click.Path(exists=True),
    help="The source for the image data. Can be a file, directory, url or stdin.",
)
@processor
def overlay_cmd(images, file):
    yield from image_handler(images, overlay)
