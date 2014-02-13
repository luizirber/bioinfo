#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''bioinfo

Collection of scripts for bioinformatics problems.

Usage:
  bioinfo bam_coverage <reference> <alignments> <minmatch> <query> [--mapq=<n>]
  bioinfo -h | --help
  bioinfo --version

Options:
  --mapq=<n>    Minimum MAPQ quality [default: 30].
  -h --help     Show this screen.
  --version     Show version.
'''

from __future__ import unicode_literals, print_function, division
from docopt import docopt

from .bam_coverage import bam_coverage


__version__ = "0.1.3"
__author__ = "Luiz Irber"
__license__ = "BSD License"


AVAILABLE_COMMANDS = {
    'bam_coverage': bam_coverage,
}


def main():
    '''Main entry point for the bioinfo CLI.'''
    args = docopt(__doc__, version=__version__)

    if 'bam_coverage' in args:
        bam_coverage(args['<reference>'],
                     args['<alignments>'],
                     int(args['<minmatch>']),
                     args['<query>'],
                     min_mapq=int(args['--mapq']))

if __name__ == '__main__':
    main()
