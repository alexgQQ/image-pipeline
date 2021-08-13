import numpy as np
import cv2

from PIL import Image
from functools import update_wrapper


def image_handler(images, func, *args, **kwargs):
    to_cv = kwargs.pop('to_cv', False)

    for image in images:
        filename = image.filename

        if to_cv:
            mode = image.mode
            if mode == 'RGB' or mode == 'P' and image.palette.mode == 'RGB':
                cv2_convert = cv2.COLOR_BGR2RGB
                mode = 'RGB'
            elif mode == 'RGBA' or mode == 'P' and image.palette.mode == 'RGBA':
                cv2_convert = cv2.COLOR_BGRA2RGBA
                mode = 'RGBA'
            image = cv2.cvtColor(np.array(image), cv2_convert)

        image = func(image, *args, **kwargs)

        if to_cv:
            image = cv2.cvtColor(image, cv2_convert)
            image = Image.fromarray(image).convert(mode)

        image.filename = filename

        yield image


def processor(f):
    """
    Helper decorator to rewrite a function so that it returns another
    function from it.
    """

    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


def generator(f):
    """
    Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """

    @processor
    def new_func(stream, *args, **kwargs):
        yield from stream
        yield from f(*args, **kwargs)

    return update_wrapper(new_func, f)

