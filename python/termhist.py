#!/usr/bin/env python3

import click
import numpy as np
import termplotlib as plt

@click.command()
@click.argument('infile', type=click.File())
@click.option('--range', 'hist_range', nargs=2, type=float, help='Min and max of the histogram')
@click.option('--bins', type=int, help='Number of bins in the histogram')
def do_plot(infile, hist_range, bins):
    """

    To pipe in data from STDIN pass in '-' to INFILE.

    Plot a histogram on the command line.

    If --bins is not specified, the bins are calculated using the `sqrt` method
    of `numpy.histogram`, which performs reasonably for most data sets.

    """

    fig = plt.figure()

    dat = np.loadtxt(infile)

    if bins is None:
        bins = 'sqrt'

    fig = plt.figure()
    hist, bins = np.histogram(dat, bins=bins, range=hist_range)

    fig.hist(hist, bins, orientation="horizontal", force_ascii=False)
    fig.show()



if __name__ == '__main__':
    do_plot()
