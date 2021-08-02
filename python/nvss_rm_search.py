#!/usr/bin/env python3

import click
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u


@click.command()
@click.argument('nvss_cat', type=click.File())
@click.argument('ra', type=str)
@click.argument('dec', type=str)
@click.argument('radius', type=float)
def cone_search(nvss_cat, ra, dec, radius):
    """
    Given the input NVSS RM catalog and a source RA and DEC this performs a cone search within the given RADIUS and prints
    out all the matches.

    The RADIUS must be specified in degrees.

    RA and DEC must be of the format HHhMMmSS.SSs DDdMMmSS.SSs

    The RM catalog can be obtained here - http://www.ras.ucalgary.ca/rmcatalogue/RMCatalogue.txt
    """

    try:
        target_coord = SkyCoord(f'{ra} {dec}')
    except ValueError as e:
        print("Invalid format for RA and/or DEC")
        raise e

    df = pd.read_csv(nvss_cat, delim_whitespace=True, header=None)
    ra = [f"{hh}h{mm}m{ss}s" for hh, mm, ss in zip(df[0], df[1], df[2])]
    dec = [f"{dd}d{mm}m{ss}s" for dd, mm, ss in zip(df[5], df[6], df[7])]

    dfcoords = SkyCoord(ra, dec)
    df['coords'] = dfcoords
    df['coords'] = df['coords'].map(lambda x: x.to_string('hmsdms'))

    #df = df[['coords', 12, 15, 18, 21]]

    sep = dfcoords.separation(target_coord)

    radius = radius * u.degree
    idx = np.where(sep <= radius)
    df = df.iloc[idx]

    ndf = pd.DataFrame()
    ndf = ndf.reset_index(drop=True)
    ndf['coordinates'] = df['coords']
    ndf['int_flux (mJy)'] = df[12].astype("str") + df[13].astype("str") + df[14].astype("str")
    ndf['peak_pol (mJy)'] = df[15].astype("str") + df[16].astype("str") + df[17].astype("str")
    ndf['frac_pol (mJy)'] = df[18].astype("str") + df[19].astype("str") + df[20].astype("str")
    ndf['RM'] = df[21].astype("str") + df[22].astype("str") + df[23].astype("str")

    print(ndf.to_string(index=False))

    #print("Coordinates         Integrated Flux (mJy)        Peak Pol flux (mJy)            % Pol        RM")
    #for row in df.iterrows():
    #    print(row)
    #    print(row[24].to_string('hmsdms'), row[12], row[15], row[18], row[21])



if __name__ == '__main__':
    cone_search()
