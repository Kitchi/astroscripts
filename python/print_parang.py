#! /usr/bin/env python

import click

@click.command()
@click.argument('name', type=str)
@click.argument('beg_time', type=str)
@click.argument('end_time', type=str)
@click.argument('coord_ra', type=str)
@click.argument('coord_dec', type=str)
@click.option('--timezone', default='Etc/GMT0',
              help='Time zone (default: Etc/GMT0)')
def print_parangs(name, beg_time, end_time, coord_ra, coord_dec, timezone):
    """
    Prints the parallactic angle range given the start and end observing
    times (in UCT/GMT), the telescope name and the celestial target
    coordinates.

    Currently accepted telescope names : uGMRT or MeerKAT (case insensitive)

    The beg time and end time should be in the format '2020-01-01T00:00:00'

    The target coordinates must be in HMS DMS (i.e., 00h00m00s +00d00m00s)
    """

    from astroplan import Observer
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astropy.time import Time

    import numpy as np

    if name.lower() == 'ugmrt' or name.lower() == 'gmrt':
        obs = Observer(longitude = '74d02m59s' , latitude = '19d05m47s' ,
                       elevation = 0*u.m, name = 'uGMRT', timezone=timezone)
    elif name.lower() == 'meerkat':
        obs = Observer(longitude = '21d26m38s' , latitude='-30d42m39.8s',
                       elevation = 1086.6*u.m , name = 'MeerKAT',
                       timezone=timezone)
    elif name.lower() == 'alma':
        obs = Observer(longitude = '67d45m12s' , latitude='-23d01m09s',
                       elevation = 0*u.m , name = 'ALMA',
                       timezone=timezone)
    else:
        raise NotImplementedError("Unknown telescope name")


    coord = SkyCoord(coord_ra, coord_dec)

    beg_time = Time(beg_time)
    end_time = Time(end_time)

    parang_beg = np.rad2deg(obs.parallactic_angle(beg_time, coord))
    parang_end = np.rad2deg(obs.parallactic_angle(end_time, coord))

    print("Beginning parallactic angle {:.3f}".format(parang_beg))
    print("Ending parallactic angle {:.3f}".format(parang_end.deg))

    print("Parang delta {:.3f}".format(parang_end - parang_beg))

if __name__ == '__main__':
    print_parangs()
