#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# © 2018 The Board of Trustees of the Leland Stanford Junior University
# Nathaniel Watson
# nathankw@stanford.edu
###

"""
For the provided DCC experiment identifiers, writes out the unique set of associated genetic_modification
accessions to the specified output file, one per line.
"""

import argparse
import datetime
import json
import os
import pdb

import encode_utils.connection as euc
from encode_utils.parent_argparser import dcc_login_parser

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        parents=[dcc_login_parser],
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", "--outfile", required=True, help="Output file name.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--records", default=[], nargs="+", help="""
      One or more DCC experiment identifiers. """)
    group.add_argument("-i", "--infile", help="""
      An input file containing one or more DCC experiment identifiers, one per line. Empty lines and
      lines starting with '#' are skipped. """)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    rec_ids = args.records
    infile = args.infile
    outfile = args.outfile
    # Connect to the Portal
    dcc_mode = args.dcc_mode
    if dcc_mode:
        conn = euc.Connection(dcc_mode)
    else:
        # Default dcc_mode taken from environment variable DCC_MODE.
        conn = euc.Connection()
    if not rec_ids:
        # Then get them from input file
        fh = open(infile)
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rec_ids.append(line)
    gms = []
    for i in rec_ids:
        rec = conn.get(i)
        for rep in rec["replicates"]:
            for gm in rep["library"]["biosample"]["genetic_modifications"]:
                gm = gm.strip("/").split("/")[-1]
                if gm not in gms:
                    print(gm)
                    gms.append(gm)
    fout = open(outfile, "w")
    for i in gms:
        fout.write(i)
    fout.close()

if __name__ == "__main__":
    main()
