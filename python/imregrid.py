#!/usr/bin/env python3

import os
import sys
import shutil

import click
import numpy as np

from casatasks import imregrid
from casatools import image
ia = image()

import logging

# Add colours for warnings and errors
logging.addLevelName(logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-20s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

def wipe_file(filename):
    if os.path.exists(filename):
        shutil.rmtree(filename)


ctx = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=ctx)
@click.argument('template', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True))
@click.option('-f', '--force', 'do_force', is_flag=True, help='Force overwriting output if already exists.')
def do_imregrid(template, target, do_force):
    """

    Run the CASA task imregrid to scale the TARGET image to match the TEMPLATE
    image.

    The input images can be either FITS images or CASA images.

    This script depends on CASA 6.
    """

    target_name, ext = os.path.splitext(target)
    outname = target_name + '_scaled' + ext

    if os.path.exists(outname):
        if do_force:
            print(f"WARNING : Image {outname} exists, forcing overwrite")
        else:
            print(f"Image {outname} exists, --force not passed, not overwriting.")
            print(f"Exiting.")
            exit(0)

    ia.open(template)
    template_shape = ia.shape()
    ia.close()

    templatecoord = imregrid(template)

    ia.open(target)
    target_shape = ia.shape()
    outcsys = ia.coordsys().torecord()
    ia.close()

    if target_shape[0] % 2:
        crpix = [target_shape[0]//2 + 1, target_shape[1]//2 + 1]
    else:
        crpix = [target_shape[0]//2, target_shape[1]//2]

    target_units = outcsys['direction0']['units']
    template_units = templatecoord['csys']['direction0']['units']

    # make sure units match before regridding, otherwise it will fail
    if template_units[0] == target_units[0]:
        pass
    elif template_units[0] == "'" and target_units[0] == 'rad':
        # Convert from rad to arcmin
        outcsys['direction0']['units'] = template_units
        outcsys['direction0']['cdelt'] *= (180/np.pi)
        outcsys['direction0']['cdelt'] *= 60.
    elif template_units[0] == "rad" and target_units[0] == "'":
        # Convert from arcmin to rad
        outcsys['direction0']['units'] = template_units
        outcsys['direction0']['cdelt'] /= 60.
        outcsys['direction0']['cdelt'] *= (np.pi/180.)

    outcsys['direction0']['crpix'] = np.asarray(crpix).astype(int)
    outcsys['direction0']['crval'] = templatecoord['csys']['direction0']['crval']
    outcsys['direction0']['latpole'] = templatecoord['csys']['direction0']['latpole']
    outcsys['direction0']['longpole'] = templatecoord['csys']['direction0']['longpole']

    tmpname = 'tmp.im'
    wipe_file(tmpname)
    shutil.copytree(target, tmpname)

    ia.open(tmpname)
    ia.setcoordsys(outcsys)
    ia.close()

    imregrid(tmpname, template=templatecoord, output=outname, overwrite=True, axes=[0,1], interpolation='cubic', decimate=10)

    wipe_file(tmpname)


if __name__ == '__main__':
    do_imregrid()
