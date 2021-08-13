import click
import numpy as np
import cv2

from .utils import processor, image_handler


def cluster(image, clusters=5):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0
    )
    ret, label, center = cv2.kmeans(Z, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))


@click.command('cluster')
@click.option(
    '-n', '--clusters', default=5, show_default=True
)
@processor
def cluster_cmd(images, clusters):
    ''' Cluster an image. '''

    yield from image_handler(images, cluster, to_cv=True, clusters=clusters)
