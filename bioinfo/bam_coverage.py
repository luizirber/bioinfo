#! /usr/bin/env python
"""
Usage:

   bam-coverage.py reference.fa query.x.reference.bam minmatch query.fa mapq

bam-coverage calculates the fraction of bases in 'reference.fa' that are
covered by a BAM alignment file, for sequence in 'query.fa' that are
longer than 'minmatch'.

Original script: https://github.com/ngs-docs/ngs-scripts/blob/master/blast/calc-blast-cover.py
"""

from __future__ import print_function, division
import sys

DEPENDENCIES = {
    "pysam": False,
    "screed": False
}

try:
    import pysam
    DEPENDENCIES['pysam'] = True
except ImportError:
    pass

try:
    import screed
    DEPENDENCIES['screed'] = True
except ImportError:
    pass


def check_dependencies():
    if all(DEPENDENCIES[d] for d in DEPENDENCIES):
        return True

    print("Missing dependencies, install before proceeding:", file=sys.stderr)
    for dep, installed in DEPENDENCIES.items():
        if not installed:
            print(dep, file=sys.stderr)

    sys.exit(1)


def bam_coverage(reference, alignments, min_match, query, min_mapq=30, min_len=0):
    check_dependencies()

    # load in the query sequences into a list
    print("reading query", file=sys.stderr)
    query_seqs = set([r.name for r in screed.open(query)
                      if len(r.sequence) >= min_match])

    # create empty lists representing the total number of bases in the
    # reference
    print("creating empty lists", file=sys.stderr)
    covs = {}
    for record in screed.open(reference):
        covs[record.name] = [0] * len(record.sequence)

    # run through the BAM records in the query, and calculate how much of
    # the reference is covered by the query.
    print('building coverage', file=sys.stderr)
    with pysam.Samfile(alignments, "rb") as samfile:
        for record in samfile:

            if record.qname not in query_seqs:
                continue

            if record.mapq < min_mapq:
                continue

            cov = covs.get(samfile.getrname(record.tid))
            if not cov:
                continue

            if min_len and len(record.aligned_pairs) < min_len * len(record.seq):
                continue

            for pos_read, pos_ref in record.aligned_pairs:
                if pos_ref:
                    cov[pos_ref] = 1

    # print out summary statistics for each of the reference.
    coved = {}
    sizes = {}
    total = 0
    covered = 0
    print('Summing stats', file=sys.stderr)
    for name in covs:
        coved[name] = sum(covs[name])
        sizes[name] = float(len(covs[name]))
        covered += coved[name]
        total += sizes[name]
    fraction = covered / float(total or 1)

    print('total bases in reference:', total)
    print('total ref bases covered :', covered)
    print('fraction                :', fraction)
    print('reference               :', reference)
    print('BAM alignment file      :', alignments)
    print('query sequences         :', query)

    return {
        'total': total,
        'covered': covered,
        'fraction': fraction,
        'coverage per contig': coved,
        'contig size': sizes
    }


if __name__ == "__main__":
    reference = sys.argv[1]
    alignments = sys.argv[2]
    min_match = int(sys.argv[3])
    query = sys.argv[4]
    min_mapq = int(sys.argv[5])

    bam_coverage(reference, alignments, min_match, query, min_mapq=30)
