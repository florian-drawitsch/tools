#!/usr/bin/env python
"""Crops up and writes image into tiles of specified size."""

import os
import argparse
import numpy as np
from PIL import Image

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('source', type=str)
p.add_argument('width', type=int)
p.add_argument('height', type=int)
args = p.parse_args()

def main(source, width=256, height=256):

    source_splitext = os.path.splitext(source)
    img = Image.open(source)

    x_steps = int(np.floor(img.size[0]/width))
    y_steps = int(np.floor(img.size[1]/height))
    j = 0
    for ix in range(x_steps):
        for iy in range(y_steps):
            area = (ix*width+1, iy*height+1, (ix+1)*width, (iy+1)*height)
            img.crop(area).save(source_splitext[0] + '_crop_{:03d}'.format(j) + source_splitext[1])
            j += 1
            
if __name__ == '__main__':
    main(**vars(args))