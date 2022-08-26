#!/usr/bin/env python

import scipy as sp
import numpy as np

from scipy.signal.signaltools import correlate2d as c2d
from scipy.misc import imread

from skimage.color import rgb2gray
from skimage.exposure import equalize_hist
from skimage import io as io
from skimage.filter import threshold_otsu, threshold_adaptive
from skimage.morphology import disk,erosion

import matplotlib.pyplot as plt


def binerize_image(image_array):
    binerised_image = np.where(image_array > np.mean( \
    image_array), 1.0, 0.0)
    return binerised_image


def plot_image(image_array):
    plt.imshow(image_array)
    plt.show()


def normalize(image_array):
    normalised_image = (image_array - image_array.mean()) \
    / image_array.std()

    return normalised_image


def scipy_w3c_luminance(image_array):
    greyscaled = sp.inner(image_array, [299, 587, 114]) / 1000.0

    return greyscaled


def compare_image(image_base, image_comp):
    """base_image = imread(image_base)
    comp_image = imread(image_comp)"""

    base_image = io.imread(image_base)
    comp_image = io.imread(image_comp)


    block_size = 40
    base_image = threshold_adaptive(base_image, block_size, offset=10)
    comp_image = threshold_adaptive(comp_image, block_size, offset=10)
    #plot_image(base_image)
    #plot_image(comp_image)


    #convert to grey scale
    base_image_grey = rgb2gray(base_image)
    comp_image_grey = rgb2gray(comp_image)



    #hist equalize
    base_image_grey = equalize_hist(base_image_grey)
    comp_image_grey = equalize_hist(comp_image_grey)

    #Binerize image
    base_image_grey = binerize_image(base_image_grey)
    comp_image_grey = binerize_image(comp_image_grey)

    #normalize
    base_image_norm = normalize(base_image_grey)
    comp_image_norm = normalize(comp_image_grey)


    #2d Correlation
    base_line = c2d(base_image_norm, base_image_norm, mode='same')
    base_to_new_comp = c2d(base_image_norm, comp_image_norm, mode='same')
    differ = base_line.max() - base_to_new_comp.max()
    print base_line.max(), base_to_new_comp.max(), differ


if __name__ == "__main__":
    compare_image("bo_1.jpg", "bo_1.jpg")