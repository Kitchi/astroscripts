#!/usr/bin/env python3

import click
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle

import matplotlib.pyplot as plt


@click.command()
@click.argument('target_ra')
@click.argument('target_dec')
@click.argument('npoint', type=int)
@click.argument('sep', type=float)
@click.option('--katopt', is_flag=True, help='Print out source list in a form KAT OPT can understand')
@click.option('--srcprefix', type=str, default='', help='Prefix for source names in grid')
def grid_pointings(target_ra, target_dec, npoint, sep, katopt, srcprefix):
    """
    Script to generate the pointing positions to sample an NxN grid around a
    given target location.

    TARGET_RA and TARGET_DEC is the location of the central pointing, nominally
    the source around which the mosaic is intended. They should be specified in
    the format XXhXXmXX.XXs and XXdXXmXX.XXs or in decimal degrees.

    NPOINT is the number of pointings on one side of the grid mosaic.

    SEP is the separation (in arcmin) between each pointing.

    WARNING : This script uses the *linear* approximation to angle offsets, so
    it will start accumulating large errors for large offsets.
    """

    # Check that the coordinates are alright. If the coordinates are specified in decimal radians it will
    # still work, but that is up to the user to get right.
    try:
        ph_centre = SkyCoord(target_ra, target_dec)
    except UnitsError:
        try:
            ph_centre = SkyCoord(float(target_ra), float(target_dec), unit='degree')
        except ValueError:
            msg = 'Coordinates must be in hexagesimal or decimal degrees. Format not recognized.'
            raise ValueError(msg)

    halfn = npoint//2

    if npoint % 2:
        do_central_pointing = True
    else:
        do_central_pointing = False

    new_pos_list = []
    for rr in range(npoint):
        dra = Angle((rr - halfn) * sep, unit='arcmin')
        for dd in range(npoint):
            ddec = Angle((dd - halfn) * sep, unit='arcmin')

            new_ra = ph_centre.ra - dra
            new_dec = ph_centre.dec - ddec

            new_pos = SkyCoord(new_ra, new_dec)
            new_pos_list.append(new_pos)

    if katopt:
        ffile = open('katopt.csv', 'w')
        ffile.write('# name, tags, ra, dec (J2000)\n')
        for idx, nn in enumerate(new_pos_list):
            ffile.write('%s%03d, ' % (srcprefix, idx))
            ffile.write('radec target, ')

            rh = int(np.floor(nn.ra.hour))
            delta = nn.ra.hour - rh
            rm = int(np.floor(delta * 60.))
            delta = delta*60. - rm
            rs = delta * 60.

            dd = int(np.floor(nn.dec.deg))
            delta = nn.dec.deg - dd
            dm = int(np.floor(delta * 60.))
            delta = delta*60 - dm
            ds = delta*60.

            ffile.write('%02d:%02d:%.2f, %02d:%02d:%.2f\n' % (rh, rm, rs, dd, dm, ds))
        ffile.close()
    else:
        for nn in new_pos_list:
                print(nn.to_string('hmsdms'))

    plt.scatter([nn.ra.deg for nn in new_pos_list], [nn.dec.deg for nn in new_pos_list])
    plt.xlabel("RA (deg)")
    plt.ylabel("DEC (deg)")
    plt.show()




if __name__ == '__main__':
    grid_pointings()
