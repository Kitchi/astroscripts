#! /usr/bin/env python

import argparse
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import SymLogNorm

from casatools import image 
ia = image()

def kill_ripple():
    parser = argparse.ArgumentParser(description='Kill ripple in a CASA image.')
    parser.add_argument('image', type=str, help='Input CASA image file')
    parser.add_argument('--npeaks', type=int, default=1, help='Number of peaks in the FFT to remove (default: 1)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output, and diagnostic plots')
    parser.add_argument('--outfile', type=str, default=None, help='Output file name for the modified image (default: None)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the output file if it exists')

    args = parser.parse_args()

    if args.verbose:
        print(f"Reading data")
    ia.open(args.image)
    dat = ia.getchunk()[:,:,0,0]
    ia.close()

    if args.verbose:
        print(f"Taking fft")
    fftdat = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(dat)))

    cx, cy = np.array(fftdat.shape) // 2

    for nn in range(args.npeaks):
        peak_loc = np.unravel_index(np.argmax(np.abs(fftdat)), fftdat.shape)
        delta_x = peak_loc[0] - cx
        delta_y = peak_loc[1] - cy

        # Greab the peak and its hermitian conjugate counterpart
        peak_locs = [(cx + delta_x, cy + delta_y), (cx - delta_x, cy - delta_y)]

        if args.verbose:
            print(f"Peak location: {peak_locs}")

        for loc in peak_locs:
            fftdat[loc] = 0.0

    ifftdat = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(fftdat))).real

    if args.verbose:
        print(f"Plotting")
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        ax[0].imshow(dat, cmap='viridis', origin='lower', norm=SymLogNorm(linthresh=1e-5, vmin=-0.01, vmax=0.1))
        ax[1].imshow(ifftdat, cmap='viridis', origin='lower', norm=SymLogNorm(linthresh=1e-5, vmin=-0.01, vmax=0.1))
        plt.tight_layout()

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.imshow(np.abs(fftdat), cmap='viridis', origin='lower)
        ax.set_title('FFT Magnitude')
        plt.show()

    if args.outfile:
        outname = args.outfile
    else:
        outname = args.image.replace('.image', '_ripple_killed.image')

    if args.verbose:
        print(f"Writing output to {outname}")

    if not args.overwrite and os.path.exists(outname):
        raise FileExistsError(f"Output file {outname} already exists. Use --overwrite to overwrite it.")

    if args.overwrite and os.path.exists(outname):
        if args.verbose:
            print(f"Output file {outname} already exists, overwriting it.")
        shutil.rmtree(outname, ignore_errors=True)

    shutil.copytree(args.image, outname)
    ia.open(outname)
    ia.putchunk(ifftdat[:, :, np.newaxis, np.newaxis])
    ia.close()




if __name__ == '__main__':
    kill_ripple()
