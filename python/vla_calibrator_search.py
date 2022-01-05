#!/usr/bin/env python

import click
import datetime
import numpy as np
import pandas as pd

from astropy.coordinates import SkyCoord
import astropy.units as u

from bs4 import BeautifulSoup
import requests


def vla_cal_to_text(url, persist=False):
    """
    Scrape the VLA Calibrator Manual website and store as plain text
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    now = datetime.datetime.now()
    now = now.isoformat()
    fname = f'vla_calibrator_manual_{now}.txt'

    if persist:
        with open(fname, 'w') as fptr:
            fptr.write("\n")

    allentries = []

    smallsoup = soup.find_all('pre')
    for ss in smallsoup:
        caltext = ss.text
        allentries.append(caltext)

        if persist:
            with open(fname, 'a') as fptr:
                fptr.write(caltext)
                fptr.write("\n")

    return allentries


def print_source_matches(cal_manual, srcpos, rad):
    """
    Prints out all matching sources within rad degrees of srcpos.

    cal_manual is assumed to be a list of strings, where each string contains
    the entire entry from the VLA Calibrator Manual.
    """

    for entry in cal_manual:
        lines = entry.split('\r\n')
        epoch_idx = [idx for idx, line in enumerate(lines) if 'J2000' in line]

        if len(epoch_idx) > 1:
            for num, line_idx in enumerate(epoch_idx):
                epochline = lines[line_idx]
                ra = epochline.split()[3]
                dec = epochline.split()[4]
                dec = dec.replace("''", "\"")

                calpos = SkyCoord(ra, dec, equinox='J2000')
                sep = srcpos.separation(calpos)

                if sep <= rad:
                    print("\n".join(lines[line_idx:epoch_idx[num+1]]))

ctx = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=ctx)
@click.argument('RA', type=str)
@click.argument('DEC', type=str)
@click.argument('RAD', type=float)
@click.option('--persist', is_flag=True, help='Save the calibrator manual to a text file')
def scrape_vla_cal_list(ra, dec, rad, persist):
    """
    Given the input RA and DEC (in sexagesimal or decimal degrees) and the
    search radius RAD (in degrees) searches through the VLA calibrator list and
    prints out all matching sources, including the ancillary information.

    If the --persist flag is specified, the entire calibrator manual will be
    written to a text file, which will be named
    vla_calibrator_manual_<current_date_time>.txt
    """

    vla_cal_url = 'https://science.nrao.edu/facilities/vla/observing/callist'

    try:
        ra = float(ra)
        dec = float(dec)
        srcpos = SkyCoord(ra, dec, unit='degree')
    except ValueError:
        srcpos = SkyCoord(ra, dec)

    rad = rad * u.degree

    cal_manual = vla_cal_to_text(vla_cal_url, persist)

    print_source_matches(cal_manual, srcpos, rad)


if __name__ == '__main__':
    scrape_vla_cal_list()
