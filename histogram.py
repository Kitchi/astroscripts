#! /usr/bin/env python

import sys
import click
import numpy as np
import matplotlib.pyplot as plt


ctx = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=ctx)
@click.argument('inpdata', type=click.File('r'), default=sys.stdin)
def plot_hist(inpdata):
    """
    Plot a histogram of the input data from stdin
    """

    data = np.genfromtxt(inpdata)

    hist, bins = np.histogram(data, bins='auto')

    bins = (bins[1:] + bins[:-1])/2.
    width = 0.7 * (bins[1] - bins[0])

    plt.style.use('seaborn-poster')
    fig, ax = plt.subplots()
    ax.bar(bins, hist, width=width)
    plt.show()

if __name__ == '__main__':
    plot_hist()
