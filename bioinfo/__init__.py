#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''bioinfo

Usage:
  bioinfo bwa_coverage <reference> <bwa_alignment> <minmatch> <query> [--mapq=<n>]
  bioinfo -h | --help
  bioinfo --version

Options:
  --mapq=<n>    Minimum MAPQ quality [default: 30].
  -h --help     Show this screen.
  --version     Show version.
'''

from __future__ import unicode_literals, print_function, division
from docopt import docopt

__version__ = "0.1.0"
__author__ = "Luiz Irber"
__license__ = "MIT"


def main():
    '''Main entry point for the bioinfo CLI.'''
    args = docopt(__doc__, version=__version__)
    if 'bwa_coverage' in args:
        from .calc_bwa_cover import calc_bwa_coverage

        calc_bwa_coverage(args['<reference>'],
                          args['<bwa_alignment>'],
                          int(args['<minmatch>']),
                          args['<query>'],
                          min_mapq=int(args['--mapq']))

if __name__ == '__main__':
    main()
