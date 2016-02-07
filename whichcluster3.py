from PIL import Image
import glob, os
import numpy as np

def convertsmall(infile):
    size = 40,40
    im = Image.open(infile)
    im.thumbnail(size)
    pixels = np.asarray(im)
    pixels1=np.copy(pixels)
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            if pixels1[i][j]>127:
                pixels1[i][j]=0
            else:
                pixels1[i][j]=1
    return pixels1





