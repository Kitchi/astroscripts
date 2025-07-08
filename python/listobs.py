#! /usr/bin/env python

import os
import argparse
from casatasks import listobs

def run_listobs():
    """
    Given an input MS, or list of MSs - run listobs on them.
    """

    parser = argparse.ArgumentParser(description="Run listobs on the input Measurement Set(s).")
    parser.add_argument('ms', nargs='+', help='Input Measurement Set(s) to list observations from.')
    parser.add_argument('--outdir', type=str, default=None, help='Output directory for the listobs files. Default is to place them in the same directory as the MSs.')

    args = parser.parse_args()

    for ms in args.ms:
        if not os.path.exists(ms):
            print(f"Error: The specified Measurement Set '{ms}' does not exist.")
            continue

        outdir = args.outdir if args.outdir is not None else os.path.dirname(ms)
        
        # Create output file name based on the MS name
        msname = os.path.basename(ms)
        outfile = os.path.join(outdir, f"{msname}.listobs")

        print(f"Running listobs on {ms} and saving output to {outfile}")
        try:
            listobs(vis=ms, listfile=outfile)
        except Exception as e:
            print(f"Error running listobs on {ms}: {e}")
            continue

if __name__ == '__main__':
    run_listobs()
