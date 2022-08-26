#!/usr/bin/env python
__author__ = '357808'

import scipy as sp
from scipy.misc.pilutil import imread
from scipy.signal.signaltools import correlate2d as c2d
import pylab


def get_image_data(image_file):
    """
    Read image and convert to vector
    """
    img_tmp = imread(image_file)
    #pylab.imshow(img_tmp)

    data = sp.inner(img_tmp, [299, 587, 114]) / 1000.0
    return (data - data.mean()) / data.std()



def compare_score(imfile_base,imfile_new):
    """
    Compare two images
    """
    #sp.resize()
    base_data = get_image_data(imfile_base)
    new_data = get_image_data(imfile_new)

    basline = c2d(base_data,base_data,mode='full')

    compare_score_ = c2d(base_data,new_data,mode='full')

    difference =  basline.max() - compare_score_.max()

    print basline.max(), compare_score_.max(), difference

if __name__ == "__main__":
    base_image = "al_1.jpg"
    comp_img = "al_2.jpg"
    compare_score(base_image,comp_img)